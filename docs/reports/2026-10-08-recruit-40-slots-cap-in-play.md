# Recruit unit: the 40-recruited-units cap in play (row L11, 40 recruited units)

**Provenance:** draft from `diegoami/ic2-conquest`, branch `main`, commit
`52fd7b3` (`52fd7b38e45e54391d27ae94f070cd7cab24f8c6`); run data at `fee951a`.
Release
[`run-exp-l11-40-recruit-slots`](https://github.com/diegoami/ic2-conquest/releases/tag/run-exp-l11-40-recruit-slots)
holds `T_RECRUIT_40SLOTS.SAV`, and its SHA-256 is committed at
`runs/experiments/data/run-exp-l11-40-recruit-slots/SAVES.sha256`. Wine-only evidence.
Companion to the inventory row L11
([`2026-10-05-player-facing-feature-inventory.md`](2026-10-05-player-facing-feature-inventory.md))
and to R46 / RC01 in [`2026-10-05-refusal-texts-and-conditions.md`](2026-10-05-refusal-texts-and-conditions.md).
RC01 staged only the 40th slot (nation 0 +0x420 = 1). This run fills **all 40 slots**
and checks that the queue does not grow.

**Review note:** the slot layout in the method (8-byte slots from nation +0x2E4:
state, type, troops, city) puts slot 39's troops at +0x2E4 + 39 × 8 + 4 = +0x420.
That is the address R46's gate reads (L55949), so the pre-state hits the field
the code tests. The box text comes from OCR (`'…lint of 40 units…'`), and it
matches R46's literal.

**Tag:** `[confirmed, partial]` for the "40 recruited units" bullet of L11 (Recruit
unit at one city; mercenary hire and other cities not run).

## Answer

- With Rome's 40 recruitment slots all occupied, a 41st **Recruit unit** order is refused with the box *"You have reached your limit of 40 units."* (R46, `TArmyRecruits_RecruitUnit`:56033).
- The queue stays at 40 occupied slots at city 85 (Rome), before and after: nothing is queued.

| Slots occupied before | Order | Box | Slots occupied after |
|---:|---|---|---:|
| 40 (all at city 85) | Recruit unit, Rome, heavy infantry, 2 (thousands) | "You have reached your limit of 40 units." | 40 |

Evidence: `T_RECRUIT_40SLOTS.SAV` (sha256 `aca5cebb84d41eee…`, release `run-exp-l11-40-recruit-slots`); `runs/experiments/data/run-exp-l11-40-recruit-slots/test_run_1.log` and `SAVES.sha256`. The test is `tests/test_orders.py` `recruit_40_slots_cap`. It first passed at `6bddb39` (`tests/results.md`, "2026-10-08, L11 40-recruited-units gate regression") and passed again for this draft (51 s).

## Method

- Pre-state: `_make_patched_save_full_slots(BASE, nation_index=0, city_id=85, n_slots=40, state=12, typ=1, troops=3200)`. Each of Rome's 40 slots at nation +0x2E4 (8 bytes: state, type, troops, city) gets (12, heavy infantry, 3,200, city 85). BASE.SAV is 270 BC Spring week 1 with Rome human.
- Fast rollingsave seed exe, seed 12345, Xvfb :99. Load, save, check 40 occupied slots at city 85, issue `g.recruit(city_row=1, unit_type="hi", thousands=2)`, capture the box text, save, and count the slots again.
- The gate in code (R46): slot 39's troops (nation +0x420) must be below 1, so a full queue is detected by its last slot.

## Not established

- The mercenary path (`TRecruitMercs_RecruitMercUnit`), which L11 also cites.
- Whether the gate tests only slot 39 (R46's reading) or the whole queue. A save with slots 0-38 empty and slot 39 occupied (RC01) refuses as well, which is consistent with the slot-39 test. Settled since: the mirror case (slot 0 empty, slots 1-39 occupied) is refused too, so the gate reads slot 39 only ([`2026-10-08-recruit-40-slots-gate-reads-slot-39.md`](2026-10-08-recruit-40-slots-gate-reads-slot-39.md)).
