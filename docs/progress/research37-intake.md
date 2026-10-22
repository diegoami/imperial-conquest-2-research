# Research37 SAV export intake running notes

Plan: verify the pinned ic2-conquest PR #100 source packet against source, public saves, DAT and bounded original x86; promote only the partial safety result; correct related serialization prose; keep the writer and Windows gate open.

Owner choice: Codex Sol medium subagent implements. The quota service suggested MiniMax M3 (rank 1, spare seven-day capacity, reliability factor 0.962); this suggestion did not select the implementer. Owner selected Gemini Flash for the independent PR review; the parent session will run it after this handoff.

Progress — commit 1: independently checked the v2 matrix (33 contiguous regions, 1,172 bytes, 31 UNKNOWN), 14 public SHA256 saves and 224 nation owned-city lists/baselines, DAT hash and 16 profiles, source hash and all 1,111 focused lines. Reran ten original-x86 controls on the pinned executable; generated JSON exactly matches the retained v2 result. Promoted the partial report, corrected the old serialization layout, and updated ledger, evidence index, rules summary, pending gate and README count. `git diff --check` and relative-link checks passed. No private owner saves, candidate exports or Windows outputs were supplied to this intake; no live game was run.

## Reproducible intake receipt

All packet paths below are at ic2-conquest `ac958a0fa58984098641a7992a42d0fbf517d473` under `runs/experiments/data/run-exp-sav-export37/`. Their SHA256s at intake:

| Artifact | SHA256 |
|---|---|
| `nation-matrix-v2.csv` | `7a087d53d2e1b983834a39a928c63f298c3efd0dd9ca0ece69c1a2769abc5fd5` |
| `public-scalar-audit-initial.json` | `7824735f2f8f56a2bf22db69f769a44fd36815f46ef1bb88ede914b9d4bcdce4` |
| `dat-profile-initial.json` | `cb1ae4b78332249d41c33b89e381fdeb6a73f353d8b3fcb61b8ae694fe7fbba6` |
| `source-focused-v1.txt` | `bf229a5cc6c64e37d7cbc3ad8f5f5d35d7d12a1db371914193bcc03aabcda9e2` |
| `x86-controls-v2.json` | `69d640e9ee224dd6e9878fb083196a248e5c793770325d78dc5a04af7164c6da` |

The independent raw-save decoder read each of the fourteen filenames in `public-scalar-audit-initial.json` from the tracked ic2-conquest `saves/` directory and checked its SHA256 before parsing. It found army count as little-endian signed WORD at absolute `100956`, skipped `100958 + 656*army_count` to the fleet count, then skipped `2 + 26*fleet_count` to the sixteen 1,172-byte nation records. It decoded all 334 city owners from city-record `+18` at `89600 + 34*city_id`; each nation record's current count at `+446` and 334 signed city IDs at `+048`; and asserted each active list equals the owned city IDs sorted by raw ASCII city-name bytes, with every inactive ID `-1`. All 224 records passed. In each record, `+450..46A`, `+46D` and `+491..493` were zero in this sampled family; that observation does not establish a default. The decoder directly compared current population/treasury at `+430/+438` with historical fields `+434/+43C`, and checked the three historical values against sixteen independently decoded DAT records (`0x1B100 + 1055*n`, baseline offsets `+1033/+1037`, count `+1047`). All 224 historical triples matched; current treasury differed from its historical baseline in 131 records. The DAT SHA256 was `94d0ccfc67148d727de4c4e60aefc3c53ba9e67775bd689f0fcb2e23c12e5fbd`.

The independent matrix parser converted each hex `first,last` pair to an inclusive interval, checked the declared byte length, and asserted their concatenation equals `range(1172)`. Exactly 33 intervals cover the record without gaps or overlap; three `UNKNOWN_REJECT_CHANGED_STATE` intervals total 31 bytes. The original whole-source SHA256 was `2018c205a4e4ea4a4079f2d166623fb571062832d76e19b72e11d1f0edac87d8`; every one of the 1,111 numbered focused lines matched that source at its original line number. This is a source/extract identity check, not exhaustive read-path analysis.

The bounded control rerun used the pinned recovery layout and wrote only a new `/tmp` result:

```bash
cd /home/diego/projects/ic2-work/sav-export37/conquest
python3 runs/experiments/sav_export37/controls.py --output /tmp/sav37-controls-intake.json
python3 runs/experiments/sav_export37/validate_packet.py --output /tmp/sav37-packet-intake.json
```

The ten-control result was JSON-equal and SHA256-equal (`69d640e9ee224dd6e9878fb083196a248e5c793770325d78dc5a04af7164c6da`) to the retained v2 file: ten passes, zero errors. The offline packet validator reported 14 saves, 224 records, 247 functions, 2,040 references, 1,111 focused lines, ten controls, 33 regions, 1,172 bytes and 31 UNKNOWN bytes, with `Windows_output_round_trips: 0` and `changed_state_export_readiness: false`. Neither command ran the game or produced an exported SAV.

Progress — commit 2: made the independent check receipt durable with pinned packet hashes, raw offset and assertion method, and bounded x86 reproduction command.

END: research #37 and main #1194/T185 remain open; three native Windows output round trips and changed-state semantics remain unmet. Task #25 and immutable fixtures were not changed. PR review and merge belong to the parent session.


## Native tax observation and current-gates promotion (2026-10-21)

The earlier END/0-output statement above is historical. This follow-up promotes
ONLY the requested native-tax draft and current-gates status from conquest
main7fe20bedba0b9cdbb012b1b348c96507f6a65768. Native blob749755e9b38b74b365669c002c2e522170530fa9;
status blob3bde157c4217183a32a7f05fed69babe53ae5b01. Native remains identical
to PR104c8193ca; full Kimi review/dispositions at95d906e3 read (static/private
path limits,three nonblocking notes). Status PR106 reviewed0e9457e/final631d105e;
complete GLM report/dispositions read; aggregate inventory is reported-only.

Owner: main Codex/OpenAI session implements, GLM5.3Flash independently reviews,
retaining this session's explicit choices; commit/push without another question.
Previously live-verified route opencode-go/glm-5.3-flash on native OpenCode1.18.32
fallback. No replacement model or quota choice inferred (suggestion unavailable).
Own worktree branchintake/37-native-tax, basef698190d65bf3c6cc3445cfb0982301e4202fae9.

Plan: check exact draft blobs,latest packet/validator and writer delivery;
rehash accessible private sources without copying; attempt no-game validator;
check committed scalar chains and strict guard; write bounded native report,
fold aggregate status/four gates into pending requests,add superseding notes,
ledger/evidence/progress/count; validate public diff; PR/review/approved merge;
keep37open and post short promotion-commit link for main evidence pipeline.

Validation so far:
- Packet README/v3 is current; draft v2link/334JSON count stale. V2/v3 same
  input/stage/capture/check records; historicalv3 parsed336JSON and38PNGhashes;
  current committed tree337JSON includes v3 itself. All337parse, six Python
  modules inspected/compile check available without executing UI orchestration.
- Exact verify_native_packet.py attempted unchanged with isolated Python and
  bytecode disabled, normal and unsandboxed. Recorded source path unavailable;
  same function retried with SOURCE relocated to accessible current fixtures,
  then stops at unavailable candidates. NO validation output/PASS produced.
  Dated native evidence is ACCESS DENIED even direct known-file opens/native
  read-only probes; do not call it deleted or infer absence. No ACL/ownership
  modification,game/GUI/bridge action or private-byte copying.
- All3 accessible sourceSAV digests and runtimeEXE digest freshly match published
  values. Candidate digests match writer8c31728 production-delivery comment
  https://github.com/diegoami/imperial-conquest-2-research/issues/37#issuecomment-6247428351
  and v3/completions/controls. This is documentary candidate provenance, not
  a fresh candidate-byte check; no delivery manifest was recoverable locally.
- New metadata-only checker validates recorded3case chains,initial/candidate
  equality,three distinct phase digests,reopen identity,ordinary recruit effects,
  controls2/3 and control1's5changed bytes. Actual v3assert tested with3synthetic
  phase patterns. Normal and optimized checker results equal; an in-memory
  L==E==R corruption is rejected. Allprivate stage/capture byte claims remain
  upstream observations. Metadata checker is not the private validator.
- Control1 before/after=tax+area left/top; source/baseline additionally moves
  Information window; candidate/final-control=8geometry bytes,not tax difference.
  No extra gameplay-byte changes in published full-span record; no callback
  movement cause inferred. Preserve blank case1capture,case3one-confirmation
  continuation and ad-hoc UI/script-coverage limits.

Reproduce committed-record check from repository root:
`python3 -I scripts/sav37-native-metadata-check.py CONQUEST_CHECKOUT --output NEW.json`.
It reads exact7fe20be Git blobs only,never private SAV/PNG/JSON inventory, and
refuses an existing output. Full no-game private validator remains separately
required wherever retained source/candidate/native-output access is available;
choose NEW output and do not run UI orchestration or rewrite old measurements.

Progress — author commit: report with requested bounded native tag/tables/limits;
current-gates folded into pending37,old0/3paragraph preserved with superseding
3/3tax/0/12nativeJSON note; both ledger commit/blob pins; scalar-only evidence
index/receipt/checker; README189. No private paths/native-JSON hashes/inventory,
original bytes,private saves or PNGs enter researchGit. Allbranch scan applies
only for candidate visibility; unrelated drafts are not promoted.

END (author candidate)
- Work remains: independent exact-head GLM review,approved merge,short issue37
  link with promotion SHA and peer acknowledgment. No downstream Evaluated marker
  or T184–T186/#1191 completion asserted; main owns evaluation/routing.
- Native tax gate3/3 OBSERVED; nativeJSON gate0/12,callbackUNVERIFIED,UNKNOWN31
  unknown,#37OPEN. Fresh full private-byte rerun blocked by actual evidence access.


### Readable owner-copy follow-up (before independent PR review)

Initial failures above are retained as history, now superseded for private-byte
verification. Owner provided readable retained copies outside researchGit.
Fresh21SAV+38PNG lengths/hashes match the historicalv3 manifest59/59; four extra
copied files are not silently counted as manifested evidence. Original writer
folder/candidate basenames/manifests remain unavailable. Bound candidate names
were supplied as temporary links OUTSIDEGit to retained Itransport copies; their
fresh SHA256s match fixed production-delivery digests. SOURCE and PRIVATE were
explicitly relocated; verify_native_packet.main FUNCTION BYTE-UNCHANGED, no
assertion/input repair, candidate regeneration or input-byte copying byintake.

Actual no-game validator EXIT0/PASS:3cases,337current measurementJSON,38capture
hashes,0active originals; all casechecks/immutable-input/stage/capture/EXErecords
exactly equal retainedv3. Current337 vs historical336 includes v3itself. Source
and EXE hashes checked afresh. Additional independent whole-byte comparisons:
all3I/L pairs,all3E/R pairs,controls2/3after==candidate copies; control1 tax+
area5byte mask, source/baseline Information4bytes, candidate/finalcontrol8geometry
bytes all match. Captures hash-checked, not visually replayed. No game,GUI,
bridge,save creation,ACL/ownership change or research-private input copy.

Updated final candidate report/superseding notes/ledger/evidence/receipt before
review; native3/3 and JSON0/12 limits unchanged. Earlier commit8a05910/draftPR48
captured inaccessible-input state, not the final verification claim. This next
commit records the successful rerun and retained-copy provenance honestly.

END (updated author candidate)
- Pending: independent exact-head GLM review/approved merge,short issue37 link.
- Main evidence pipeline owns Evaluated/routing intoT184–T186/#1191.
- Native tax3/3 observed; nativeJSON0/12; callbackUNVERIFIED;UNKNOWN31;37OPEN.


### Author raw-save field-label correction during the same review

Independent raw L/O/E/R decoding confirms all3queue/treasury/mobilization/
calendar values. It catches one inherited draft label error: case3before entry
[24,0,0,0] uses(state,type,troops,city), so24is first/stateWORD and typeWORD0;
original UI replaces it with[0,0,3000,85]. Report/scalar receipt corrected;
no meaning/default inferred for inactive state24. Ordinary totals/native3/3
unchanged. The in-progress GLM client was interrupted and its returned text
read; resume SAME session ses_e9fc448fdffer68N42uWq5reJa/model on correctedhead,
not a fresh review/model. Full interruption/continuation record kept outsideGit.

### Completion receipt added for cloud continuation (2026-10-21)

PR48 merged at `16f019397e65ba521bbcee7acea2a7d2c9bd7c93`. The same owner-selected
GLM5.3Flash session completed its interrupted coverage at author head
`4d20d8b014ed6c37d0957ee34896276453a79ef3`; its complete
[final review](https://github.com/diegoami/imperial-conquest-2-research/pull/48#issuecomment-6326559898)
was read and returned APPROVE with two nonblocking notes. The reviewer checked
source/receipts and metadata, not private bytes or pixels; the author's separate
private-byte validator rerun is recorded above. No original writer manifests were
recovered. This supersedes the earlier pending-review/merge instructions.

[Research37 promotion comment](https://github.com/diegoami/imperial-conquest-2-research/issues/37#issuecomment-6326579112)
links the merge. Tax-only native3/3, nativeJSON0/12, callbackUNVERIFIED and UNKNOWN31
remain unchanged; research37 is open. No downstream Evaluated marker or
T184–T186/#1191 routing is asserted. See
[../cloud-continuation.md](../cloud-continuation.md) for the durable cloud checkpoint.

### Gate 2 export policy intake (2026-10-22)

The owner confirmed this intake after the IC2 Conquest session's relay
(ic2-conquest `80a3963`, PR #130).
- **Reproduction:**
  - the checker test passes;
  - the 28 public per-file receipts reproduce byte for byte;
  - the private-bundle identity group counts reproduce, with only counts recorded.
- **New controls:** `scripts/gate2-policy-adversarial.py` canonicalises 15 saves (all accepted)
  and applies 13 mutation types. Every type is refused except the missing or out-of-range
  allegiance, which the checker does not enforce.

Report: [2026-10-22-sav-export-gate2-policy](../reports/2026-10-22-sav-export-gate2-policy.md).
Gates 1, 3 and 4 are unchanged, and research #37 stays open.

The allegiance defect was fixed upstream in `2fd663a` (PR #131). Research reran its controls
(`gate2-policy-adversarial-v2.json`): 0 unexpected results, and no original verdict changed.
