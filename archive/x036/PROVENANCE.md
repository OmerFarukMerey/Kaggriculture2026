# X036 submission provenance

X036 composes three frozen components:

1. Kaito Fukami's Apache-2.0 Community V1 route, SHA-256
   `9bdfbafb6755067182d88ce594fd46fb1d712713ffd6931e83d5d50e84bc6fb2`.
2. Our V1.1.1 observation-confirmed FEED/WATER retry layer, SHA-256
   `5f0d98a453866092fe78c9464845b7685c5b8ab9d4167a0459b683cba6b899cf`.
3. The X030 milk ridge model generated from all 41 downloaded public episodes,
   alpha 10 and the frozen public day-10 feature schema. Generated module
   SHA-256: `91b325430a0b82f953dd61837d0e520abf34d7327c69510e26a1846637d09c51`.

The policy threshold is exactly `28.86780869330488` predicted milk units. At or
below that value, X034 moves one existing `SELL MILK 3` order from day 11 hour 0
to hour 1 after observation-confirming stock. Above it, the policy is exact
V1.1.1 behavior.

Evidence is recorded in `xperiments.md` and `artifacts/x030`, `x034`, `x035`,
and `x036`. X036 passed its one-shot seeds 5-24 Pareto-safe confirmation before
packaging. No leaderboard episode or private information is a runtime feature.
