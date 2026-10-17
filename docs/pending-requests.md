# Pending research requests

Requests from other sessions that are accepted but not done. Whoever picks one up (any session)
removes it here when its report is promoted, and tells the requester.

## Desktop palette check (with the player, via ic2-conquest)

Asked by the research session on 2026-10-09 (the user asked). Every marker-colour result so far is
Wine-only: [`2026-10-09-owner-colours-by-band.md`](reports/2026-10-09-owner-colours-by-band.md),
[`2026-10-09-city-marker-colours.md`](reports/2026-10-09-city-marker-colours.md) and
[`2026-10-09-unit-icon-recolour-and-nation-glyphs.md`](reports/2026-10-09-unit-icon-recolour-and-nation-glyphs.md).

**Steps** (ic2-conquest `runs/experiments/data/run-exp-desktop-palette/STEPS.md`): on the Windows
original, load `colours_PRE.SAV` (`run-exp-owner-colours`) and `cities_PRE.SAV`
(`run-exp-city-marker-colours`). Use the same view, take a screenshot of the map and of the
toolbar's nation buttons, and note the display's colour depth.

**Also asked:** where the 2026-09-29 strip of
[`2026-09-29-nation-marker-colours.md`](reports/2026-09-29-nation-marker-colours.md) was cropped
from (toolbar, raw glyph bitmaps, or map), and on which system. The current reading, that it
came from raw glyphs with the white transparent margin visible, is `[derived]`.

**Expected:** the glyphs and image lists carry their own palettes, so the desktop should draw the
same 16 colours. Numidia's grey unit fill is in the code's colour table, so it should be grey
on the desktop too.

**Done when:** a desktop draft is promoted, or the player declines. Remove this entry then.

## Tactical target/draw divergences (research #25)

The prerequisite gate is now cleared at reviewed build PR #1156, merge
`257f2d2cd7510451d229a983553a54b89065b06c`, including the control correction
alongside #1103/#1105. The 318-hook comparison and recovered historical inventory
are promoted as [confirmed, partial](reports/2026-10-16-tactical-target-and-draw-attribution.md).

At that pin: 282 complete exact, 36 residual; 283 exact draw sequences. The old
42-series recovered working survey contains the historical 57-case/41-series
registry set plus `hi-ar-three_s3_r5_hook`; later 63/48 and post-T175 90 target/draw
registry entries are different snapshots/counting units, not residual series counts.

**Fresh original progress:** the [decision trace](reports/2026-10-16-tactical25-original-decision-trace.md)
reproduces all 325 legacy draw tuples and all 15 full saves in both runs, with NEW original
claims/pass observations. At half-round 6, Gaul slot 22, original and port share all decoded
slots/names, grid and equivalent claim counts immediately before choosing goals;
original (5,3) versus port (6,4) is attributable to the actor-versus-enemy archer
condition. Rankings already differ at half-round 4 but choose the same goal there. This is
an observed shared-input decision cause, not a verified full corrected battle.

**Still open:** complete corrected battle matching for all 36 residual paths. Nineteen series
have a reproduced local rule discrepancy on a model phase input, seventeen have
none in the evaluated probes. Original runtime claims and the general pass of
original shots are not in legacy logs/SAVs; these gaps cannot be filled by local
x86 execution on model state. Retain the state-only `ar-hi-three_s3` residual.

The requested `mix-rg_s1` starting case is now pinned: draw 24, HR6, site
`0x439557`, original Gaul23 -> Rome2 `Random(1085)=357`, model Gaul22 -> Rome1
`Random(172)=56`. The changed actor/target pair prevents treating it as a simple
range correction. Local threat aim/order differs, but complete causality is not proved.

**Next:** evaluate a bounded actor/enemy threat-key correction against the pinned
source rules, then perform a separately reviewed sensitivity/full comparison and
identify exactly which complete residual paths disappear. The new original trace
supplies claims/pass input through HR6 for mix-rg_s1 only; it does not fill missing
legacy fields or the other cases. Further original observations may still be needed
for other paths and the 24 stopped-before-shot Pass2 stages. Preserve immutable
fixtures/draw bounds and strict comparison behavior; no gameplay, expected-failure
or fixture change is authorized merely by promoting this report.

**Done when:** a reviewed report establishes the surviving complete causal paths.
Partial rule findings remain evidence for build evaluation; unexplained cases and
research #25 / build #1107 stay open until that attribution is established.

## SAV export semantic and native Windows gate (research #37)

The [partial safety finding](reports/2026-10-17-sav-export-live-regions-and-safe-rejection-policy.md) establishes the live city list, historical baselines, 31 UNKNOWN nation bytes and constructor residue. It does not clear changed-state export. Main #1194/T185 stays open. An unchanged authentic identity path still requires complete-state and framing/version validation; same-template lineage does not establish safe changed-state inheritance.

**Next:** establish the missing semantic/record-residue policy and produce applicable candidate exports without modifying private originals. With owner coordination and a native Windows runtime, open at least three distinct representative outputs, inspect state, perform an ordinary action/end turn, save each to a new copy and reopen. Preserve private inputs/outputs outside code repositories; record approved redacted/scalar evidence. No owner-private inputs, candidate paths or coordinated Windows run were supplied to this intake. Wine and self-reader checks do not satisfy this gate. Task #25 remains a separate open request above.
