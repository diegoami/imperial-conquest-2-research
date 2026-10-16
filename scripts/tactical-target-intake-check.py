"""Cross-check a pinned tactical25 capture against raw original hooks and saves.

Usage: python3 scripts/tactical-target-intake-check.py EVIDENCE_DIR FIXTURES_ROOT
EVIDENCE_DIR is runs/experiments/data/run-exp-tactical25 at ic2-conquest 586d3613.
Only canonical production/phases directories and top-level text inputs are needed.
No original runtime, .NET production comparison or x86 instructions are executed.
"""
import argparse,collections,csv,hashlib,json,pathlib,re,struct
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('evidence',type=pathlib.Path);p.add_argument('fixtures',type=pathlib.Path)
a=p.parse_args(); D=a.evidence; F=a.fixtures/'battles'
def load(name):return json.loads((D/name).read_text())
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def lowword(n):return (n+32768)%65536-32768
fixture_hashes={}
for line in (F/'SHA256SUMS').read_text().splitlines():
    sha,name=line.split(maxsplit=1)
    fixture_hashes[name.removeprefix('*').removeprefix('./')]=sha
def pinned(path):
    assert digest(F/path)==fixture_hashes[path],path

manifest=load('evidence-manifest-20261016-1813.json');checked=0
canonical=('production-20261016-174818/','phases-20261016-180904/','phases-20261016-180932/')
for name,sha in manifest['files'].items():
    if '/' not in name or name.startswith(canonical):
        path=D/name
        assert path.is_file(),name
        assert digest(path)==sha,name
        checked+=1
root=D.parents[3]
for name,sha in manifest['sources'].items():assert digest(root/name)==sha,name
print('Pinned canonical/top-level text hashes:',checked,'and',len(manifest['sources']),'source hashes')
for capture in ['production-20261016-174818','phases-20261016-180904','phases-20261016-180932']:
    m=load(capture+'-manifest.json')
    assert m['build_head']=='257f2d2cd7510451d229a983553a54b89065b06c'
    assert m['fixtures_head']=='6319802a75067e7730e4f6a27dce3b4e296ddd9b'
    assert m['exit']==0 and m['source_clean_after'] and m['no_fixture_or_rule_edits']
s=load('production-20261016-174818/summary.json');inv=load('inventory-20261016-181249.json')['rows']
assert len(s['rows'])==318 and len({r['trial'] for r in s['rows']})==318
assert sum(r['exact'] for r in s['rows'])==s['exact']==282
assert sum(r['blocks_passed'] for r in s['rows'])==s['blocks_exact']==282
assert sum(r['draws_match'] for r in s['rows'])==s['draws_exact']==283
assert len(inv)==s['residual']==36
assert {r['trial'] for r in inv}=={r['trial'] for r in s['rows'] if not r['exact']}
sites=collections.Counter();all_draws=0;originals={}
for row in s['rows']:
    assert row['pairing_error'] is None
    hook=F/row['hook'];pinned(row['hook']);assert digest(hook)==row['hook_sha256'],row['trial']
    with hook.open(newline='') as f: records=list(csv.DictReader(f))
    orig=[];indices=[]
    for i,r in enumerate(records):
        if r['kind']!='random':continue
        r={k:(int(v,16) if k=='site' else int(v) if k not in ('kind','ebp') else v) for k,v in r.items()}
        assert r['seed_after']==(r['seed_before']*0x08088405+1)&0xffffffff
        assert r['result']==((r['seed_after']*r['eax'])>>32)
        orig.append(r);indices.append(i)
    model=load('production-20261016-174818/'+row['trial']+'-draws.json')
    assert len(orig)==row['original_draw_count'] and len(model)==row['model_draw_count']
    assert all(d['index']==i for i,d in enumerate(model))
    limit=min(len(orig),len(model));idx=next((i for i in range(limit) if (orig[i]['eax'],orig[i]['result'])!=(model[i]['bound']&0xffffffff,model[i]['value']&0xffffffff)),limit)
    equal=idx==len(orig)==len(model)
    assert equal==row['draws_match'],row['trial']
    fd=row['first_divergence']
    if not equal:
        assert fd is not None and fd['draw_index']==idx
        assert fd['original']==orig[idx]
        assert (fd['model']['bound'],fd['model']['value'],fd['model']['counter'])==(model[idx]['bound'],model[idx]['value'],model[idx]['counter'])
        assert fd['source_site']==hex(orig[idx]['site'])
        sites[fd['source_site']]+=1
        pos=indices[idx]
        if orig[idx]['site']==0x439188:
            marker=next(r for r in reversed(records[:pos]) if r['kind']=='marker' and int(r['site'],16)==0x43910c)
            actor,target=lowword(int(marker['eax'])),lowword(int(marker['edx']))
        else:
            markers=[r for r in records[pos:] if r['kind']=='marker' and int(r['site'],16)==0x438fb0][:2]
            assert len(markers)==2
            actor,target=[lowword(int(r['eax'])) for r in markers]
        assert (actor,target)==(fd['original_actor']['unit'],fd['original_actor']['target']),row['trial']
        assert (model[idx]['actor']['unit'],model[idx]['actor']['target'])==(fd['model_actor']['unit'],fd['model_actor']['target'])
        assert fd['original_claims'] is None
    else:assert fd is None
    assert row['exact']==(row['post_and_conclusion_passed'] and row['draws_match'] and row['peace_match'])
    all_draws+=len(orig);originals[row['trial']]=row
assert sites=={'0x439557':30,'0x439188':4,'0x4395ce':1}
print('Raw original hooks: 318 hashes,',all_draws,'RNG records; 283 equal range/result streams, 35 first draw divergences and actor pairs checked')
def h(b,o):return struct.unpack_from('<h',b,o)[0]
def turn(path):
    b=path.read_bytes();o=100958+h(b,100956)*656;o+=2+h(b,o)*26+16*1172+600
    t=o+2+(h(b,o)+1)*61;week,year,season=struct.unpack_from('<3h',b,t+40)
    return (300-year)*24+season*6+(week-1)//2
for r in inv:
    pinned(r['start']);assert r['turn']==turn(F/r['start'])==743
    row=originals[r['trial']];assert r['first_draw']==row['first_divergence']
    assert r['original_runtime_claims'] is None
    if r['first_draw'] is not None:assert len(r['model_claims_at_first_draw'])==40
    match=re.search(r'hook/([^ ]+\.SAV).*slot (\d+), (\w+): port (-?\d+), original (-?\d+)',r['first_state_difference'])
    assert match,r['trial']
    name,slot,field,port,original=match.groups();slot=int(slot);pinned('hook/'+name)
    b=(F/'hook'/name).read_bytes()[-2105:]
    offset={'x':0,'y':1,'origin':2,'type':3,'troops':4,'quality':5,'morale':6,'moves':7,'shots':8,'target':9}[field]
    assert h(b,9+44*slot+2*offset)==int(original)
    phase=load('phases-20261016-180932/'+r['trial']+'.json')
    assert phase['validated_entire_state_and_log'] and phase['counter']==r['first_state_counter']
    assert phase['stages'][-1]['after']['slots'][slot][field]==int(port),(r['trial'],field)
    assert int(port)!=int(original)
print('36 raw first-state differences and turn-0743 starts checked, including state-only ar-hi-three_s3')
probes=load('original-threat-20261016-180959.json')
assert len(probes['rows'])==30 and len(probes['pass_two'])==108
completed=[r for r in probes['pass_two'] if r['status']=='pure original pass completed']
assert len(completed)==84
pt={r['trial'] for r in completed if r.get('differences')};th={r['trial'] for r in probes['rows'] if r['aim_differs']}
assert (len(pt),len(th),len(pt&th),len(pt|th))==(6,15,2,19)
assert len({r['trial'] for r in inv}-(pt|th))==17
print('Local-probe inventory: 84 completed/24 stopped Pass2 stages, 30 threat inputs; 19 discrepancy series/17 without in these probes')
repro=load('original-repros-20261016-180225.json');model=load('phases-20261016-180932/model-repros.json')
matrix=repro['matrix'];assert matrix==model['matrix']
def weighted(troops,q,m,typ,enemy):return ((troops*q)//100)*m*matrix[typ*5+enemy]
assert [weighted(3000,5,70,1,0),weighted(4000,1,50,0,1),weighted(3000,5,70,1,1),weighted(2000,9,90,1,1)]==[630000,8000,52500,81000]
assert (2*8000)//3<630000 and not (2*81000)//3<52500
assert repro['rows'][0]['original_target']==20 and model['weighted_pass2_target']==21
keys=[450,300,300,150];order=[20,21,22,23]
for i in range(3):
    least=min(range(i,4),key=lambda j:keys[j])
    keys[i],keys[least]=keys[least],keys[i];order[i],order[least]=order[least],order[i]
assert order==probes['minimal_sort']['order'][:4]==[23,21,22,20]
assert model['sort_order']==[23,22,21,20]
assert probes['minimal_archer_subject']['order'][:2]==[21,20] and model['archer_subject_order']==[20,21]
assert probes['minimal_flank_equal_y']['destination']==[3,3] and model['flank_destination']==[3,7]
print('Synthetic weighted-strength arithmetic, suffix-minimum tie order and paired local reproduction outputs checked')
history=load('historical-survey-reconciliation.json')
assert digest(D/'survey-with-walk-order-experiment.tsv')==history['source_sha256']=='41f71b7061b5034576731f79c5b18297b7d7704c3e705b90ff9b31c37dab19e0'
with (D/'survey-with-walk-order-experiment.tsv').open(newline='') as f:survey=list(csv.reader(f,delimiter='\t'))
assert len(survey)==636
true=[r for r in survey if r[0]=='True'];assert len(true)==318
# Mode is column 0; completion depends on the ratio and absence of differences.
def completed(r):
    passed,total=map(int,r[3].split('/'))
    return passed==total and not r[4].strip() and not r[6].strip() and r[9]=='drawsAll:'
assert sum(completed(r) for r in true)==276
incomplete={r[1] for r in true if not completed(r)}
assert len(incomplete)==42 and incomplete==set(history['survey_incomplete_series'])
historical={r['FirstDifference'].split(':')[0] for r in load('registry-t129-9664936e.json') if r['Issue']==1107}
current={r['FirstDifference'].split(':')[0] for r in load('registry-baseline-5ca9c3f.json') if r['Issue']==1107}
assert incomplete-historical=={'hi-ar-three_s3_r5_hook'} and not historical-incomplete
assert incomplete-current=={'hi-ar-three_s3_r5_hook'} and current-incomplete==set(history['current_only_vs_survey'])
print('Recovered survey: 636 rows, 318 emulation-mode rows, 276 complete / 42 incomplete; exact missing-series reconciliation checked')
for filename,expected in [('registry-t129-9664936e.json',(57,41)),('registry-baseline-5ca9c3f.json',(63,48))]:
    rows=[r for r in load(filename) if r['Issue']==1107]
    assert (len(rows),len({r['FirstDifference'].split(':')[0] for r in rows}))==expected
assert history['survey_only_vs_historical']==['hi-ar-three_s3_r5_hook']
print('Historical inventory 57/41 and later 63/48 checked; recovered working-survey provenance remains qualified')
print('Intake audit passed. Complete-comparison success flags, x86 execution and phase-observer equivalence are upstream evidence, not independently rerun here.')
