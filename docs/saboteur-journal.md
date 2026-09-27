# Saboteur Journal — Lab 9

## Boundary mutation

- Change: In `src/calc.py`, changed the qualifying promo condition from `len(promo_code) >= 6` to `len(promo_code) > 6` locally.
- Before restoring: `test_boundary_promo_len_6_gets_discount` and `test_qualifying_promo_overrides_every_tier` both failed. Hypothesis shrank the latter to `total=5`, `promo_code='000000'`, `tier='vip'` (expected 1, got 0).
- After restoring `>=`: `22 passed`; combined coverage 96%.
- The mutation was tested locally. A CI failure on a pushed sabotage commit remains unverified.
