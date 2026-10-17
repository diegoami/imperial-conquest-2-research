#!/usr/bin/env python3
"""Independent raw-byte intake for pushed conquest research33 packet.

Arguments: CONQUEST NEW_SAVES LEGACY_SAVES RELEASE.json LEGACY_RELEASE.json
TREE.json ORIGINAL.exe ORIGINAL.dat DUMP. Optional --fresh-x86-dir holds
land/aboard/fleet.json from separate reruns of the pinned upstream phases.py.
No Wine/native execution. No original assets or decompilation enter research git.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

p=argparse.ArgumentParser(description=__doc__)
for name in ('conquest','new_saves','legacy_saves','release','legacy_release','tree','exe','dat','dump'):
    p.add_argument(name,type=Path)
p.add_argument('--fresh-x86-dir',type=Path)
p.add_argument('--output',type=Path)
a=p.parse_args()
data=a.conquest/'runs/experiments/data/run-exp-resupply33'
j=lambda f:json.loads(f.read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
h=lambda b,o:struct.unpack_from('<h',b,o)[0]
i=lambda b,o:struct.unpack_from('<i',b,o)[0]
pin='4e4eed591ab1696e761a0cc9fafa6ba7ad50f178'
tree=j(a.tree);assert tree['sha']==pin and not tree['truncated']
blobs=[]
for e in tree['tree']:
    if e['type']!='blob' or not e['path'].startswith((
        'findings/2026-10-17-hostile-control-recruitment-treasury-ledger.md',
        'runs/experiments/data/run-exp-resupply33/','runs/experiments/resupply33/',
        'docs/review-briefs/pr96-result.md')):continue
    b=(a.conquest/e['path']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha'],e['path']
    blobs.append(e['path'])
assert len(blobs)==35
exe=a.exe.read_bytes();dat=a.dat.read_bytes();dump=a.dump.read_bytes()
assert sha(exe)=='354d8265cba1dac2a80a0a96ce76367a368e37a4e79c30eb4f0bb587b35c532f'
assert sha(dat)=='94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd'
assert sha(dump)=='2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8'
source=dump.decode().splitlines();source_count=0
for name in ('source-audit-initial.txt','ui-size-source-20261017.txt'):
    for line in (data/name).read_text().splitlines():
        match=re.match(r'^(\d+): (.*)$',line)
        if match:
            assert source[int(match[1])-1]==match[2],(name,match[1]);source_count+=1
# Resolve PE sections independently; recheck each disassembly line's instruction bytes.
pe=struct.unpack_from('<I',exe,0x3c)[0]
sections=struct.unpack_from('<H',exe,pe+6)[0]
opt=struct.unpack_from('<H',exe,pe+20)[0]
imagebase=struct.unpack_from('<I',exe,pe+24+28)[0]
sec=pe+24+opt
def code_bytes(va,size):
    for n in range(sections):
        vs,rva,rs,rp=struct.unpack_from('<4I',exe,sec+n*40+8)
        if imagebase+rva<=va and va+size<=imagebase+rva+rs:
            return exe[rp+va-imagebase-rva:rp+va-imagebase-rva+size]
    raise AssertionError(hex(va))
instruction_count=0
for line in (data/'recruitment-disassembly-20261017.txt').read_text().splitlines():
    match=re.match(r'^([0-9a-fA-F]{8})\s+([0-9a-fA-F]+)\s+',line)
    if match:
        b=bytes.fromhex(match[2]);assert code_bytes(int(match[1],16),len(b))==b
        instruction_count+=1
assert code_bytes(0x45070e,6).hex()=='298638040000'

def manifest(path):
    rows={}
    for line in path.read_text().splitlines():
        digest,name=line.split(None,1)
        assert Path(name).name==name and name not in rows,name
        rows[name]=digest
    return rows
new_hashes=manifest(data/'SAVES.sha256')
old_hashes=manifest(a.conquest/'runs/experiments/data/run-exp-resupply31/SAVES.sha256')
new_assets={x['name']:x for x in j(a.release)['assets']}
old_assets={x['name']:x for x in j(a.legacy_release)['assets']}
assert len(new_hashes)==9 and set(new_assets)==set(new_hashes)
checked_old=set()
def save(name,new):
    path=(a.new_saves if new else a.legacy_saves)/name
    raw=path.read_bytes();hashes=new_hashes if new else old_hashes;assets=new_assets if new else old_assets
    assert sha(raw)==hashes[name] and assets[name]['digest']=='sha256:'+hashes[name],name
    assert len(raw)==assets[name]['size'] and len(raw)>100956
    if not new:checked_old.add(name)
    return raw
for name in new_hashes:save(name,True)

def decode(b):
    na=h(b,100956);army=100958;fc=army+na*656;nf=h(b,fc);fleet=fc+2;nation=fleet+nf*26
    news=nation+16*1172+600;tail=news+2+(h(b,news)+1)*61
    live_army=[b[army+n*656:army+(n+1)*656] for n in range(na) if h(b,army+n*656+4)>=0]
    live_fleet=[b[fleet+n*26:fleet+(n+1)*26] for n in range(nf) if h(b,fleet+n*26+8)>=0]
    return dict(nation=nation,treasury=i(b,nation+0x438),wealth=i(b,nation+0x430),
                mobilization=h(b,nation+0x442),queues=[list(struct.unpack_from('<4h',b,nation+0x2e4+n*8)) for n in range(40)],
                cities=b[89600:100956],armies=live_army,fleets=live_fleet,
                nation_bytes=b[nation:nation+16*1172],
                turn=(300-h(b,tail+42))*24+h(b,tail+44)*6+(h(b,tail+40)-1)//2,
                current=h(b,tail+36))

result=[];summary=j(data/'summary-canonical-20261017.json')
assert summary['cases']==3 and summary['new_saves']==9
for row in summary['records']:
    kind=row['stem'].split('-')[0]
    original=save(row['stem']+'-input.SAV',False)
    before=save(row['legacy_loaded'],False);after=save(row['legacy_post'],False)
    assert before==save(row['fresh_loaded'],True) and after==save(row['fresh_post'],True)
    save(row['fresh_auto'],True)
    initial,b,e=map(decode,(original,before,after))
    assert all(initial[k]==b[k] for k in ('treasury','wealth','mobilization','queues','cities','armies','fleets'))
    loaded_ui_offset=b['nation']+13*1172+0x482
    assert len(original)==len(before)
    assert [(n,x,y) for n,(x,y) in enumerate(zip(original,before)) if x!=y]==[(loaded_ui_offset,196,192)]
    assert b['turn']==e['turn']==734 and b['current']==13 and e['current']==11
    assert b['treasury']==1000 and b['wealth']==1767000 and b['mobilization']==24
    assert all(q[2]==0 for q in b['queues'])
    assert all(b[k]==e[k] for k in ('cities','armies','fleets'))
    ledger=[];balance=1000;mobilization=24;power=0
    for n,(state,typ,troops,city) in enumerate(e['queues']):
        if troops==0:continue
        price=h(dat,0x1f2f0+40*typ+0x22);unitpower=h(dat,0x1f2f0+40*typ+0x26)
        cost=(troops//200)*price;power+=(troops//100)*unitpower
        balance-=cost;mobilization=min(100,mobilization+(troops*1000)//1767000+1)
        ledger.append(dict(slot=n,state=state,type=['li','hi','ar','lc','hc'][typ],type_index=typ,
                           troops=troops,city=city,initial_price=price,cost=cost,power=(troops//100)*unitpower,
                           dat_price_offset=hex(0x1f2f0+40*typ+0x22),original_price_address=hex(0x478fd2+40*typ)))
    assert ledger==row['ledger']
    assert [x['cost'] for x in ledger]==([128,92,330,460,435] if kind=='fleet' else [128,92,330,460])
    assert balance==e['treasury']==(-445 if kind=='fleet' else -10)
    assert mobilization==e['mobilization']==(47 if kind=='fleet' else 43)
    assert 1000-e['treasury']==sum(x['cost'] for x in ledger) and row['treasury_residual']==0
    runtime=j(data/row['runtime']);assert runtime['seed']==row['runtime_seed']==4169717509
    assert runtime['current_nation']==13 and runtime['treasuries'][0]==1000
    assert bytes.fromhex(runtime['runtime_tables'][0]['hex'])==dat[0x1f2f0:0x1f2f0+200]
    phase=j(data/f'phases-{kind}-byte-audit-20261017.json')
    assert phase['error'] is None and phase['runtime_sha256']==sha((data/row['runtime']).read_bytes())
    phases=[dict(phase=x['phase'],before=x['before']['treasuries'][0],after=x['after']['treasuries'][0]) for x in phase['phases']]
    assert phases==row['phases']
    assert phases==[dict(phase='diplomacy',before=1000,after=1000),dict(phase='recruitment',before=1000,after=balance),
                    dict(phase='army',before=balance,after=balance),dict(phase='fleet',before=balance,after=balance)]
    balance=1000
    for queue,write in zip(ledger,phase['writes'],strict=True):
        assert write['ip']=='0x45070e' and write['nation']==0 and write['frames']==['recruitment','budget_recruit']
        assert write['before']==balance and write['debit']==queue['cost']
        balance-=queue['cost'];assert write['after']==balance
    comparison=phase['post_comparison']
    assert comparison['all_nation_bytes_match'] is False
    assert comparison['nation_byte_differences']==[dict(nation=11,offset='0x482',x86=196,wine=192)]
    assert all(comparison[k] is True for k in ('queues_match','treasury_match','mobilization_match',
                                             'all_city_bytes_match','all_live_army_bytes_match','all_live_fleet_bytes_match'))
    assert h(before,b['nation']+11*1172+0x482)==708 and h(after,e['nation']+11*1172+0x482)==704
    target=15000 if kind=='fleet' else 8250
    relations=[h(before,b['nation']+0x26+n*2) for n in range(16)]
    assert relations.count(3)==1 and relations.count(2)==0
    own_power=0
    for army in b['armies']:
        assert h(army,4)==0,'These bounded controls contain no live enemy/allied armies'
        strength=0
        for slot in range(20):
            typ=h(army,16+slot*32+2);troops=h(army,16+slot*32+4)
            if troops:
                strength+=(h(dat,0x1f2f0+40*typ+0x26)*troops)//100
        own_power+=(strength//80)*h(army,14)
    assert own_power==(0 if kind=='fleet' else 6750)
    assert 15000-own_power==target
    entries=[x for x in phase['events'] if x.get('event')=='entry' and x.get('function')=='budget_recruit']
    assert len(entries)==1 and entries[0]['eax']==row['budget_target']==target
    if a.fresh_x86_dir:
        fresh=j(a.fresh_x86_dir/f'{kind}.json')
        # File-location metadata differs for fresh independent scratch outputs.
        assert {k:v for k,v in fresh.items() if k!='runtime'}=={k:v for k,v in phase.items() if k!='runtime'}
    result.append(dict(case=kind,debits=[x['cost'] for x in ledger],treasury_after=e['treasury'],
                       mobilization_after=mobilization,budget_target=target,treasury_residual=0,
                       fresh_Wine_endpoint_bytes_identical=True,nation_UI_mismatch_retained=True,
                       input_to_loaded_UI_change=dict(nation=13,offset='0x482',before=708,after=704)))
assert len(checked_old)==9
out=dict(source_branch='research/resupply33-hostile-ledger',source_commit=pin,source_merged=False,
         packet_blobs=len(blobs),source_lines_verified=source_count,disassembly_instructions_verified=instruction_count,
         new_saves_verified=9,legacy_saves_verified=9,whole_loaded_post_pairs=3,
         fresh_pinned_x86_reruns=3 if a.fresh_x86_dir else 0,cases=result,
         limits='No Wine/native run by intake; fresh x86 uses pinned upstream runner. UI difference preserved; no complete-turn/world equivalence.')
if a.output:
    with a.output.open('x') as stream:json.dump(out,stream,indent=2);stream.write('\n')
print(json.dumps(out,indent=2))
