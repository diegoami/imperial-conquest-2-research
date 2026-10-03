#!/usr/bin/env python3
"""Replay the original's New Game random draws for a given RandSeed.

FUN_00448AA4 (New Game setup) draws, in this order, from Delphi's System.Random
(FUN_0040284C: RandSeed := RandSeed * $08088405 + 1; Random(n) = (RandSeed * n) shr 32):

  1. the mercenary fill FUN_00449130, slots 0..49:
       Random(6); if > 4 then Random(9), and the slot stays empty when that is <= 7;
       a refilled slot then draws Random(200), Random(b), Random(2)
  2. the weather overlay FUN_00451304 at (Spring, week 1): N = 15, r = 4:
       for centre k = 0..19: Random(15); on 0, one Random(2) per outer-ring cell (17*17 - 9*9 = 208)
  3. the leaders: Random(12) for nations 0..15
  4. the turn order: order := [0..15]; for i = 0..15: swap(order[i], order[Random(16)])

Every Random(n) advances RandSeed once whatever n is, so only the branch draws (6, 9, 15)
decide how many draws precede the shuffle; the template sizes b do not matter.

Usage: new-game-draw-chain.py <seed> [<seed> ...]
The seed is RandSeed straight after Randomize: SEED.TXT's value on the patched build, or
UTC milliseconds since midnight on the original. Report:
docs/reports/2026-10-03-new-game-turn-order-shuffle.md
"""
import sys

NATIONS = ("Rome Carthage Seleucid Ptolemaic Macedonia Numidia Gaul Greece Celtiberia "
           "Illyria Dacia Bithynia Galatia Armenia Media Thracia").split()


def new_game(seed):
    state = seed & 0xFFFFFFFF
    count = 0

    def rnd(n):
        nonlocal state, count
        state = (state * 0x08088405 + 1) & 0xFFFFFFFF
        count += 1
        return (state * n) >> 32

    filled = 0
    for _slot in range(50):
        if rnd(6) > 4 and rnd(9) <= 7:
            continue
        rnd(200)
        rnd(1)  # Random(b): one advance whatever b is
        rnd(2)
        filled += 1
    fill_draws = count

    hits = []
    for k in range(20):
        if rnd(15) == 0:
            hits.append(k)
            for dx in range(-8, 9):
                for dy in range(-8, 9):
                    if max(abs(dx), abs(dy)) > 4:
                        rnd(2)

    leaders = [rnd(12) for _ in range(16)]
    before_shuffle = count

    order = list(range(16))
    for i in range(16):
        j = rnd(16)
        order[i], order[j] = order[j], order[i]

    return {
        "fill_draws": fill_draws, "filled_slots": filled, "storm_centres": hits,
        "leader_indices": leaders, "draws_before_shuffle": before_shuffle,
        "turn_order": order, "rand_seed_after": state,
    }


if __name__ == "__main__":
    for arg in sys.argv[1:] or ["12345"]:
        r = new_game(int(arg))
        print(f"seed {arg}: fill {r['fill_draws']} draws ({r['filled_slots']} slots filled), "
              f"storm centres {r['storm_centres']}, {r['draws_before_shuffle']} draws before the shuffle")
        print("  leader indices:", r["leader_indices"])
        print("  turn order:", r["turn_order"], "=", ", ".join(NATIONS[n] for n in r["turn_order"]))
