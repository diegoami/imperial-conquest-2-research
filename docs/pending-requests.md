# Pending research requests

Requests from other sessions that are accepted but not done. Whoever picks one up (any session)
removes it here when its report is promoted, and tells the requester.

## The original's strategic AI turn (imperial_conquest_2 #816)

Asked by IMPERIAL CONQUEST MAIN on 2026-10-06 (the owner's decision). One report, through the
findings intake (`.claude/skills/retrieve-findings/SKILL.md` for the promotion side), on:

1. The turn's shape: which routine runs a computer seat's turn, the order of its phases, per army, per city or per nation.
2. Recruiting and mobilisation: what, where, when; the treasury floor or affordability rule; how unit types are chosen; when it mobilises.
3. Movement: how an army's or fleet's destination is picked (nearest enemy city, weakest, a threatened own city); how far ahead it looks.
4. Attack and siege: which strength ratio or condition makes it attack a field army, which makes it besiege a city; how a siege ends.
5. Defence and supply: reinforcing or fortifying threatened cities, resupplying purses, repairing or scuttling fleets, hiring mercenaries.
6. Randomness (`Random(n)` uses) and human-versus-AI asymmetries.

Rules: tag every rule `[confirmed]`, `[derived]` or `[Wine candidate]` with the routine's address; name each question that stays open; never write to `imperial_conquest_2`. The EXPLORE runner (ic2-conquest) can watch AI turns on a fixed seed. Already decompiled, start from these: `decompiled-ai-offers-to-human-seats.md`, `decompiled-war-cascade-and-peace-paths.md`, `decompiled-diplomacy-peace-terms-and-instant-battles.md` (AI war declaration, alliances and trade: `FUN_0044FB7C`).

Context: the clone's AI is designed, not the original's (27 `[designed]` weights in its ruleset `ai` block); the earlier "AI out of scope" decision was reversed.

**Timing:** do not start before Claude's quota recovers (`curl -s localhost:8765/quota/claude` no longer `exhausted`; stated as Thu 2026-10-08 16:00 CEST). Not urgent, not a v0.5.0 item. Reply to IMPERIAL CONQUEST MAIN when the report is promoted.
