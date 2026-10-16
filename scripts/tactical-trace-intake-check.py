"""Read-only intake audit for the new tactical25 original decision trace.

Usage: python3 scripts/tactical-trace-intake-check.py DATA ARTIFACTS FIXTURES RELEASE_JSON
       [--source-exe ORIGINAL_SEEDED_EXE --lab-exe UNHOOKED_LAB_EXE]
DATA is runs/experiments/data/run-exp-tactical25-trace at ic2-conquest f872057.
Original saves and captures stay outside research git. This checks raw recorded bytes
and captured model states; it does not execute Wine, .NET or Unicorn, and cannot prove
that a changed port would match the entire battle.
"""
import argparse,collections,csv,hashlib,json,pathlib,struct
p=argparse.ArgumentParser(description=__doc__)
for name in ('data','artifacts','fixtures','release'):p.add_argument(name,type=pathlib.Path)
p.add_argument('--source-exe',type=pathlib.Path);p.add_argument('--lab-exe',type=pathlib.Path)
a=p.parse_args();D=a.data;A=a.artifacts;F=a.fixtures/'battles';root=D.parents[3]
def read(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(name):return read(D/name)
def csvrows(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))
manifest=load('evidence-manifest-20261016-v2.json')
for group in ('files','model_files'):
    for name,digest in manifest[group].items():assert sha(D/name)==digest,name
for name,digest in manifest['sources'].items():assert sha(root/name)==digest,name
print('Text/source/model hashes:',len(manifest['files']),len(manifest['sources']),len(manifest['model_files']))
release={x['name']:x for x in read(a.release)['assets']};hashes={}
for line in (D/'SAVES.sha256').read_text().splitlines():
    digest,name=line.split('  ',1);assert pathlib.Path(name).name==name;assert name not in hashes;hashes[name]=digest
assert len(hashes)==len(release)==len(manifest['release_checks'])==40
assert {r['local'] for r in manifest['release_checks']}==set(hashes)
assert {r['release_name'] for r in manifest['release_checks']}==set(release)
for r in manifest['release_checks']:
    digest=sha(A/r['local'])
    assert digest==hashes[r['local']]==r['sha256']
    assert release[r['release_name']]['digest']=='sha256:'+digest
print('40 local artifacts match pinned hashes and live GitHub release digests, including normalized EXE names')
old=csvrows(F/'hook/hooklog-mix-rg_s1_r5_hook.csv')
fields=('site','eax','seed_before','seed_after','result','counter','side','flag')
def tuple_(row):return tuple(int(row[k],0) for k in fields)
def decode_header(raw):
    f=struct.unpack_from('<12I',raw);top=f[0]>>24
    kind={0:'random',1:'marker',2:'flag_clear',3:'start',4:'reseed'}[top]
    site=f[0]-5 if top==0 else 0 if top==3 else f[0]&0xffffff
    return dict(seq=f[1],kind=kind,site=site,eax=f[2],edx=f[3],ecx=f[4],seed_before=f[5],seed_after=f[6],result=f[7],counter=f[8]&65535,side=f[8]>>16,flag=f[9],ebp=f[11])
fresh_logs={}
for run,validation in [('20261016-190528-1258374','validation-20261016-190814.json'),('20261016-191329-1302174','validation-20261016-191525.json')]:
    rows=csvrows(D/('hook-'+run+'.csv'));fresh_logs[run]=rows
    raw=(A/(run+'-hookbuf.bin')).read_bytes();assert len(raw)==len(rows)*48
    for i,row in enumerate(rows):
        decoded=decode_header(raw[i*48:(i+1)*48]);assert decoded['seq']==i
        assert all(decoded[k]==(row[k] if k=='kind' else int(row[k],0)) for k in decoded),(run,i)
    draws=[r for r in rows if r['kind']=='random'];legacy=[r for r in old if r['kind']=='random']
    assert len(draws)==len(legacy)==325 and [tuple_(r) for r in draws]==[tuple_(r) for r in legacy]
    for r in draws:
        before,after,bound,value=[int(r[k],0) for k in ('seed_before','seed_after','eax','result')]
        assert after==(before*0x08088405+1)&0xffffffff and value==(after*bound)>>32
    v=load(validation);assert v['pass'] and len(v['saves'])==15
    for n in range(1,16):
        name=f'BATTLE{n:02d}.SAV';assert (A/(run+'-'+name)).read_bytes()==(F/'hook'/('mix-rg_s1_r5_hook_'+name)).read_bytes()
    assert (A/(run+'-MIX-RG_start.SAV')).read_bytes()==(F/'starts/FLD-RG_0743_rome_army0_at_86_28.SAV').read_bytes()
print('Both fresh runs: raw hook buffers decode exactly; all 325 legacy tuples and all 15 whole SAVs byte-identical; unedited starts equal')
states=load('states-20261016-191329-1302174.json');assert states['overflow']==0 and len(states['records'])==152
raw=(A/'20261016-191329-1302174-statebuf.bin').read_bytes();assert len(raw)%2304==0
assert sum(bool(struct.unpack_from('<I',raw,i)[0]) for i in range(0,len(raw),2304))==152
names=('x','y','origin','type','troops','quality','morale','moves','shots','target')
byseq={}
for s in states['records']:
    b=raw[s['seq']*2304:(s['seq']+1)*2304];h=decode_header(b)
    # Snapshot Random headers are pre-call: do not treat their result/seed_after as completed draws.
    for k in ('seq','kind','counter','side','eax','edx','ecx','ebp','seed_before'):assert h[k]==s[k]
    assert hex(h['site'])==s['site']
    assert list(struct.unpack_from('<4h',b,48))==[s[k] for k in ('enemy_first','own_first','selected','active_nation')]
    assert list(b[56:60])==s['flags'] and struct.unpack_from('<I',b,60)[0]==s['original_esp']
    assert list(struct.unpack_from('<16I',b,64))==s['stack_words']
    for i,t in enumerate(s['slots']):
        assert list(struct.unpack_from('<10h',b,128+44*i))==[t[k] for k in names]
        assert b[148+44*i:172+44*i].split(b'\0')[0].decode('latin1')==t['name']
    assert list(struct.unpack_from('<168h',b,1888))==s['grid']
    assert list(struct.unpack_from('<40h',b,2224))==s['actor_claim_targets']
    byseq[s['seq']]=s
print('152 raw state snapshots decode to the published slots/names, grid, claims, flags, stack and pre-call headers')
m=load('model-phases-20261016-192217-manifest.json')
assert m['build_head']=='257f2d2cd7510451d229a983553a54b89065b06c' and m['fixtures_head']=='6319802a75067e7730e4f6a27dce3b4e296ddd9b'
assert m['exit']==0 and m['source_clean_after'] and m['no_fixture_or_rule_edits']
assert m['capture_source_sha256']==sha(root/'runs/experiments/tactical25-trace/PortPhases.cs')
assert m['driver_sha256']==sha(root/'runs/experiments/tactical25-trace/port_phases.py')
phases={n:load(f'model-phases-20261016-192217/mix-rg_s1_r5_hook-hr{n}.json') for n in range(3,7)}
attr=load('attribution-20261016-192641.json');assert len(attr['checks'])==115
fields=names+('name',)
def equal(o,m):
    return all(o['slots'][i][k]==m['slots'][i][k] for i in range(40) for k in fields) and o['grid']==m['grid'] and [o['actor_claim_targets'].count(i) for i in range(40)]==m['claims']
for check in attr['checks']:
    s=byseq[check['original_seq']];phase=phases[s['counter']];stages=phase['stages'];label=check['label'];actor=s['eax']&65535
    if label=='before target-choice helper':
        actor=s['stack_words'][1]>>16;m=next(u for u in stages[0]['units'] if u['slot']==actor)['before']
    elif label in ('after claim / before engage','before Pass1 Walk'):
        m=next(u for u in stages[0]['units'] if u['slot']==actor)['after_choice']
    elif label=='after Pass1 / before first Pass2':m=stages[1]['before']
    elif label=='after first Pass2 / before Pass3':m=stages[1]['after']
    elif label in ('before threat helper','before threat Walk'):m=next(u for u in stages[2]['units'] if u['slot']==actor)['before']
    elif label=='after threat / before nested Pass2':m=stages[3]['before']
    elif label=='after nested Pass2 / no flank / before final Pass2':m=stages[5]['before']
    elif label=='after final Pass2 / before melee slots-grid-claims only':m=stages[5]['after']
    else:raise AssertionError(label)
    assert equal(s,m)==check['equal'],(label,s['seq'])
assert min(c['original_seq'] for c in attr['checks'] if not c['equal'])==127
assert len(attr['pass1_choices'])==28
for c in attr['pass1_choices']:
    s=byseq[c['original_seq']];unit=next(u for u in phases[c['counter']]['stages'][0]['units'] if u['slot']==c['actor'])
    assert s['eax']&65535==c['actor'] and s['edx']&65535==c['original_target']==c['port_target']==unit['target']
pass1=[g for g in attr['walk_goals'] if g['stage']=='pass1'];assert len(pass1)==23
for g in pass1:
    s=byseq[g['original_seq']];goal=[s['edx']&65535,s['edx']>>16]
    assert s['site']=='0x438d24' and s['eax']&65535==g['actor']
    assert goal==g['wine_goal']==g['port_goal'] and g['equal'] and g['shared_input']
print('Recomputed all 115 original/model state comparisons, 28 Pass1 target choices and 23 Pass1 Walk goals; first unequal state seq127')
minimal=load('minimal-20261016-193117.json');assert minimal['wine']==[byseq[i] for i in (125,126,127)]
u=next(u for u in phases[6]['stages'][2]['units'] if u['slot']==22);assert u==minimal['model_unit']
assert equal(byseq[125],u['before']) and equal(byseq[126],u['before'])
assert byseq[125]['slots'][22]['type']==0 and byseq[125]['slots'][22]['shots']==7
assert byseq[125]['actor_claim_targets']==[-1]*20+[0,0,4,4,4]+[-1]*15
assert byseq[125]['flags']==[1,0,0,0]
assert [byseq[126]['edx']&65535,byseq[126]['edx']>>16]==[5,3]
assert [(d['x'],d['y']) for d in u['decisions']]==[(6,4)]
first=next(g for g in sorted(attr['walk_goals'],key=lambda g:g['original_seq']) if not g['equal'])
assert first==attr['first_observed_goal_difference']==minimal['first_goal'] and first['original_seq']==126 and first['shared_input']
assert attr['first_x86_order_difference']['counter']==4 and attr['first_x86_order_difference']['original_wine_goal']==[6,4]
pure=load('pure-original-20261016-192034.json');assert len(pure['rows'])==5
for r in pure['rows']:
    s=byseq[r['wine_walk_seq']];assert [s['edx']&65535,s['edx']>>16]==r['wine_goal']==r['original_x86_goal']
# The 115 comparisons use raw runtime claims, not inferred legacy values. Their x86 rankings remain upstream executions.
rows=fresh_logs['20261016-191329-1302174'];draws=[r for r in rows if r['kind']=='random'];r=draws[24]
assert (r['seq'],r['site'],r['eax'],r['result'])==('146','0x439557','1085','357')
next_routs=[x for x in rows if int(x['seq'])>146 and x['kind']=='marker' and x['site']=='0x438fb0'][:2]
assert [int(x['eax'])&65535 for x in next_routs]==[23,2]
assert not any(s['site'] in ('0x43910c','0x43aa88') for s in states['records'])
print('Shared-input first chosen-goal discrepancy seq126/HR6/Gaul22: original(5,3), model(6,4); ranking differs earlier HR4; fresh draw24 actor pair23->2 confirmed')
if a.source_exe or a.lab_exe:
    assert a.source_exe and a.lab_exe
    byte=load('byte-audit-20261016-194904.json');paths=[a.source_exe,a.lab_exe,A/'state-observer-20261016-191329.exe']
    exe=[x.read_bytes() for x in paths]
    for b,m in zip(exe,byte['exe_sha256s']):assert hashlib.sha256(b).hexdigest()==m['sha256']
    def section_bytes(b,va,end):
        pe=struct.unpack_from('<I',b,60)[0];assert b[pe:pe+4]==b'PE\0\0'
        count=struct.unpack_from('<H',b,pe+6)[0];opt=pe+24;size=struct.unpack_from('<H',b,pe+20)[0]
        base=struct.unpack_from('<I',b,opt+28)[0]
        for i in range(count):
            vs,rva,raw_size,raw_ptr=struct.unpack_from('<4I',b,opt+size+i*40+8)
            if base+rva<=va and end<=base+rva+raw_size:return b[raw_ptr+va-base-rva:raw_ptr+end-base-rva]
        raise AssertionError(hex(va))
    for row in byte['ranges']:
        slices=[section_bytes(b,int(row['start'],0),int(row['end_exclusive'],0)) for b in exe]
        assert slices[0]==slices[1]==slices[2]
        assert hashlib.sha256(slices[0]).hexdigest()==row['sha256']
    assert byte['ranges'][-1]['end_exclusive']=='0x44904e'
    print('Three pure-helper byte ranges match source/lab/observer EXEs, including complete distance helper through RET')
print('Audit passed. No emulator, .NET, UI or corrected-port replay executed; all36 complete battle paths remain open.')
