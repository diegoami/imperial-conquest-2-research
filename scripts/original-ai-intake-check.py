"""Independently check the October 16 original-AI evidence from raw SAV bytes.

Usage: python3 scripts/original-ai-intake-check.py ARTIFACT_DIR SAVES.sha256
       observations-20261016-153620.json RELEASE.json [--city-regions CSV]

Text inputs come from ic2-conquest commit caf2a17d420cfca35757fad60311cae9514af257,
runs/experiments/data/run-exp-ai-oct16/. RELEASE.json is the output of:
  gh release view run-exp-ai-oct16 -R diegoami/ic2-conquest --json assets
Artifacts are downloaded from that release; keep them outside research git.
This does not replay Wine, original x86 instructions, UI inputs or raw hook logs.
SAV offsets follow decompiled-sav-file-layout.md and the army/fleet field reports;
the terminal 2105-byte battle layout follows the decompiled tactical-battle report.
"""
import argparse
import hashlib,json,pathlib,struct,csv
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('artifacts',type=pathlib.Path)
parser.add_argument('manifest',type=pathlib.Path)
parser.add_argument('observations',type=pathlib.Path)
parser.add_argument('release',type=pathlib.Path)
parser.add_argument('--city-regions',type=pathlib.Path)
args=parser.parse_args()
root=args.artifacts
obs=json.loads(args.observations.read_text())
assets={a['name']:a for a in json.loads(args.release.read_text())['assets']}
assert [len(obs[k]) for k in ('supply','region','general_boundaries')]==[28,7,109], 'Incomplete pinned observation batch'
hashes={}
for line in args.manifest.read_text().splitlines():
    digest,name=line.split('  ',1)
    assert pathlib.Path(name).name==name, ('manifest path is not a bare filename',name)
    assert name not in hashes, ('duplicate manifest entry',name)
    hashes[name]=digest
for name,digest in hashes.items():
    data=(root/name).read_bytes()
    assert hashlib.sha256(data).hexdigest()==digest,name
    assert name in assets,name
    assert assets[name]['digest']=='sha256:'+digest,name
assert len(hashes)==257, 'Expected pinned 257-artifact batch'
print('Verified local bytes, pinned manifest and GitHub release digest:',len(hashes),'artifacts')
def h(b,o): return struct.unpack_from('<h',b,o)[0]
def snap(name):
    b=(root/name).read_bytes(); na=h(b,100956); off=100958+na*656; nf=h(b,off); fo=off+2; no=fo+nf*26
    army=dict(zip(('x','y','owner','moves','cell','supplies','money','morale'),struct.unpack_from('<8h',b,100958)))
    army['troops']=sum(h(b,100958+16+i*32+4) for i in range(20) if h(b,100958+16+i*32+4)>0)
    fw=struct.unpack_from('<13h',b,fo+2*26)
    fleet={k:fw[i] for k,i in [('x',0),('y',1),('supplies',7),('money',8),('condition',10),('army',11),('ships',9)]}
    return {'army':army,'fleet':fleet,'city_stock':h(b,89600+89*34+24),'treasury':struct.unpack_from('<i',b,no+0x438)[0]}
for row in obs['supply']:
    a,b=snap(row['input']),snap(row['post'])
    for field in ['army','fleet']:
        for k,expected in row[field].items(): assert [a[field][k],b[field][k]]==expected,(row['case'],field,k)
    for field in ['city_stock','treasury']: assert [a[field],b[field]]==row[field],(row['case'],field)
print('Independent raw SAV decode matches every reported subject-field pair in',len(obs['supply']),'supply/fleet cases')
for row in obs['region']:
    assert (root/row['plain_post']).read_bytes()==(root/row['observed_post']).read_bytes(),row['case']
print('Byte-identical plain/observer region pairs:',len(obs['region']))
for row in obs['general_boundaries']:
    b=(root/row['file']).read_bytes()[-2105:]
    assert h(b,4)==row['side'] and b[6]==row['phase'] and h(b,7)==row['counter'],row['file']
    live={i:struct.unpack_from('<10h',b,9+44*i) for i in range(40) if h(b,9+44*i+8)>0}
    assert set(live)=={s['slot'] for s in row['slots']},row['file']
    for s in row['slots']:
        w=live[s['slot']]
        assert (w[0],w[1],w[7],w[9])==(s['x'],s['y'],s['moves'],s['target']),(row['file'],s['slot'])
print('Independent battle-block decode matches',len(obs['general_boundaries']),'boundaries (headers, all live slots, positions/moves/targets)')
if args.city_regions:
    with args.city_regions.open(newline='') as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==334 and {int(r['city_id']) for r in rows}==set(range(334))
    boxes=[(58,64,53,61),(86,91,40,48),(82,90,49,63),(99,114,62,74),
           (149,156,54,60),(150,164,75,81),(163,167,66,71),(190,207,68,79)]
    coasts=[(44,78),(158,75),(180,36),(171,41),(163,45),(161,47)]
    for row in rows:
        x,y=int(row['x']),int(row['y']); region=-1
        for i,(x0,x1,y0,y1) in enumerate(boxes):
            if x0<x<x1 and y0<y<y1: region=i
        coast=int(not any(x<cx and y<cy for cx,cy in coasts))
        assert (region,coast)==(int(row['region']),int(row['coast_flag'])),row
    print('334-city CSV matches the transcribed classifier; this is not an x86 re-execution')
print('Intake audit passed; raw hook streams and x86 tests not independently replayed.')
