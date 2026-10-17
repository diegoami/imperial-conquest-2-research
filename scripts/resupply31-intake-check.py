#!/usr/bin/env python3
"""Independent raw-byte audit of conquest PR93's canonical resupply31 packet.

Usage: python3 scripts/resupply31-intake-check.py CONQUEST ARTIFACTS RELEASE.json
       TREE.json DUMP [--output NEW.json]

RELEASE/TREE are fresh GitHub API responses for run-exp-resupply31 and recursive
tree 27488fa4fe2a1918eff4a66f3f21fe886a67a58b. Local packet files must match that
tree. Reads only; no bot parser, Wine or emulator execution. DUMP is the original
pinned all_app_functions.txt. Original assets/extracts stay outside research git.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct

P=argparse.ArgumentParser(description=__doc__)
for name in ('conquest','artifacts','release','tree','dump'):
    P.add_argument(name,type=Path)
P.add_argument('--output',type=Path)
P.add_argument('--fresh-x86',type=Path,help='Output from a fresh run of the pinned upstream audit.py')
A=P.parse_args()
DATA=A.conquest/'runs/experiments/data/run-exp-resupply31'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
tree=load(A.tree)
assert tree['sha']=='27488fa4fe2a1918eff4a66f3f21fe886a67a58b'
assert not tree['truncated']
prefixes=('findings/2026-10-17-foreign-city-automatic-resupply.md',
          'runs/experiments/data/run-exp-resupply31/','runs/experiments/resupply31/')
blobs=[]
for entry in tree['tree']:
    if entry['type']!='blob' or not entry['path'].startswith(prefixes):continue
    content=(A.conquest/entry['path']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()==entry['sha'],entry['path']
    blobs.append(entry['path'])
assert len(blobs)==42

assert sha(A.dump)=='2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8'
lines=A.dump.read_text().splitlines()
source_lines=0
for name in ('complete-source-audit.txt','upstream-seat-source.txt'):
    for line in (DATA/name).read_text().splitlines():
        match=re.match(r'^(\d+): (.*)$',line)
        if match:
            assert lines[int(match[1])-1]==match[2],(name,match[1])
            source_lines+=1
prov=load(DATA/'complete-source-provenance.json')
for fun,(start,end) in prov['sections'].items():
    assert lines[start-1].startswith('// ==== '+fun+' @'),fun
    assert not any(l.startswith('// ==== ') for l in lines[start:end-1]),fun
    assert next(l for l in lines[end:] if l.strip()).startswith('// ==== '),(fun,end)
for calls in prov['callers'].values():
    for call in calls:assert lines[call['line']-1].strip()==call['text']

manifest={}
for line in (DATA/'SAVES.sha256').read_text().splitlines():
    digest,name=line.split(None,1)
    assert Path(name).name==name and name not in manifest,name
    manifest[name]=digest
release=load(A.release)
assert release['tag_name']=='run-exp-resupply31'
assets={e['name']:e for e in release['assets']}
assert len(assets)==len(release['assets'])
assert set(assets)==set(manifest) and len(manifest)==227
for name,digest in manifest.items():
    path=A.artifacts/name
    assert sha(path)==digest and path.stat().st_size>100956,name
    assert assets[name]['digest']=='sha256:'+digest,name
    assert assets[name]['size']==path.stat().st_size,name
for row in load(DATA/'incomplete-artifacts.json'):
    path=A.artifacts/row['name']
    assert row['name'] not in manifest and path.stat().st_size==row['size']==0
    assert sha(path)==row['sha256']


def decode(name,subject):
    assert name in manifest,name
    b=(A.artifacts/name).read_bytes()
    h=lambda o:struct.unpack_from('<h',b,o)[0]
    army=100958;na=h(100956);fc=army+na*656;nf=h(fc);fleet=fc+2;nation=fleet+nf*26
    news=nation+16*1172+600
    terminal=news+2+(h(news)+1)*61
    assert len(b)>=terminal+55
    week,year,season=(h(terminal+i) for i in (40,42,44))
    units=[army+i*656 for i in range(na)] if subject!='fleet' else [fleet+i*26 for i in range(nf)]
    owned=[o for o in units if h(o+(8 if subject=='fleet' else 4))==0]
    assert len(owned)==1,(name,owned)
    u=owned[0];s,p=(14,16) if subject=='fleet' else (10,12)
    support=dict(supplies=h(u+s),purse=h(u+p),condition=h(u+20) if subject=='fleet' else None,
                 coordinates=[h(u),h(u+2)],stocks=[h(89600+i*34+24) for i in range(334)],
                 treasuries=[struct.unpack_from('<i',b,nation+i*1172+0x438)[0] for i in range(16)])
    meta=dict(coordinates=support['coordinates'],moves=h(u+(12 if subject=='fleet' else 6)),
              turn=(300-year)*24+season*6+(week-1)//2,current=h(terminal+36),
              cell=h(u+(24 if subject=='fleet' else 8)),
              cities=[dict(id=i,x=h(89600+i*34+14),y=h(89600+i*34+16),
                           owner=h(89600+i*34+18),stock=h(89600+i*34+24)) for i in range(334)],
              relation=[h(nation+0x26+i*2) for i in range(16)],
              carriers=[struct.unpack_from('<13h',b,fleet+i*26) for i in range(nf)])
    return support,meta


def delta(b,e):
    d={k:e[k]-b[k] for k in ('supplies','purse')}
    for k,out in (('stocks','stock'),('treasuries','treasury')):
        d[out]={str(i):y-x for i,(x,y) in enumerate(zip(b[k],e[k])) if x!=y}
    if b['condition'] is not None:d['condition']=e['condition']-b['condition']
    return d


summary=load(DATA/'summary-final-20261017.json')
matrix=load(DATA/'matrix-final.json')
audit=load(DATA/'audit-final-20261017.json')
if A.fresh_x86:
    assert load(A.fresh_x86)==audit,'Fresh pinned x86 replay differs from canonical output'
matrix_rows={r['case']:r for r in matrix['records']}
rows={};log_pairs={};staging={};failures=[]
for log in sorted(DATA.glob('wine-*.jsonl')):
    before={}
    for line in log.read_text().splitlines():
        r=json.loads(line)
        if r['event']=='staged':staging[r['input']]=r
        if r['event']=='failure':failures.append((log.name,r['case'],r['exception']))
        if r['event']=='before':before[r['case']]=r
        if r['event']=='after':
            assert r['case'] not in log_pairs
            log_pairs[r['case']]=(before[r['case']],r)
for row in summary['records']:
    case=row['case'];subject=case.split(':')[0]
    assert case not in rows
    b,bm=decode(row['before'],subject);e,em=decode(row['after'],subject)
    assert b==row['initial'] and e==row['final'] and delta(b,e)==row['delta'],case
    assert b['coordinates']==e['coordinates']==[102,49] and bm['moves']==0,case
    assert bm['turn']==em['turn']==734 and bm['current']==13 and em['current']==11,case
    mr=matrix_rows[case]
    assert all(row[k]==mr[k] for k in ('before','after','turn','delta')),case
    prior,post=log_pairs[case]
    assert prior['loaded']==row['before'] and post['post']==row['after']
    for r,state in ((prior,b),(post,e)):
        f=r['fields']
        assert f['unit']['supplies']==state['supplies'] and f['unit']['money']==state['purse']
        assert f['condition']==state['condition'] and f['treasuries']==state['treasuries']
        assert f['turn']==row['turn']==734
    assert prior['fields']['current']==13 and post['fields']['current']==11
    rows[case]=(b,e,bm,em)
assert len(rows)==len(matrix_rows)==len(log_pairs)==56
assert len(failures)==2
paired=[]
for case,(b,e,bm,em) in rows.items():
    if case.startswith('aboard:') and case.replace('aboard:','land:') in rows:
        other=rows[case.replace('aboard:','land:')]
        assert (b,e)==other[:2] and bm['cell']==-1 and other[2]['cell']>=0,case
        paired.append(case.split(':')[1])
assert sorted(paired)==sorted(summary['matched_land_aboard']) and len(paired)==17
far=rows['aboard:carrier_far']
assert far[:2]==rows['aboard:peace'][:2]
assert any(f[0:2]==(150,90) and f[11]==0 and f[4]==13 for f in far[2]['carriers'])

exact=0;confounds=[];input_only=[]
for record in audit['records']:
    name=record['input'];subject=record['case'].split('-')[0]
    assert sha(A.artifacts/name)==record['input_sha256']
    assert name in staging
    if 'post' not in record:
        input_only.append(name);continue
    case=record['case'].replace('-',':',1)
    b,e,bm,em=rows[case]
    initial,im=decode(name,subject)
    assert initial==b and im['cities']==bm['cities'],case
    raw_initial={k:initial[k] for k in ('supplies','condition','stocks','treasuries')}
    raw_initial['money']=initial['purse']
    assert raw_initial==record['before'],case
    actual={k:e[k] for k in ('supplies','condition','stocks','treasuries')};actual['money']=e['purse']
    assert actual==record['wine_actual']
    expected=record['after']
    differences={k:dict(x86=expected[k],wine=actual[k]) for k in actual if actual[k]!=expected[k]}
    assert differences==record['wine_differences']
    if differences:
        assert case.endswith(':war') and set(differences)=={'treasuries'}
        assert expected['treasuries'][1:]==actual['treasuries'][1:]
        assert expected['treasuries'][0]==1000
        assert actual['treasuries'][0]==(-445 if subject=='fleet' else -10)
        confounds.append(case)
    else:exact+=1
    assert bool(record['wine_matches'])==(not bool(differences))
assert len(audit['records'])==58 and exact==53 and len(confounds)==3 and len(input_only)==2

result=dict(source_merge=tree['sha'],merged_packet_blobs=len(blobs),
            source_sha256=sha(A.dump),source_numbered_lines_checked=source_lines,
            saves_verified=len(manifest),release_digest_matches=len(assets),completed_wine_cases=len(rows),
            land_aboard_pairs=len(paired),carrier_far_matches=True,upstream_x86_inputs=len(audit['records']),
            upstream_x86_full_field_matches_reconciled=exact,hostile_buyer_treasury_confounds=sorted(confounds),
            interrupted_inputs=input_only,retained_failures=len(failures),
            fresh_pinned_x86_replay_matches=bool(A.fresh_x86),
            fresh_x86_sha256=sha(A.fresh_x86) if A.fresh_x86 else None,
            limits='No Wine/native execution by intake. Fresh x86 verification, when supplied, reruns the pinned upstream runner; the raw decoder is independent.')
if A.output:
    with A.output.open('x') as out:json.dump(result,out,indent=2);out.write('\n')
print(json.dumps(result,indent=2))
