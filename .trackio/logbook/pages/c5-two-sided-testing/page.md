# C5 — two-sided composite test

**Verdict: VERIFIED**

The implementation runs the two paper Algorithm 1 composite GLRs in parallel
and stops at their minimum; it does not use two Bonferroni-split,
known-alternative SPRTs.

Both generating sides are evaluated at three log thresholds with fifteen
trials per side and cell: 90 trials total, with zero decision errors. For both
directions, the largest-threshold normalized stopping ratio is closer to its
direction-specific `1/D_inf` coefficient than the first ratio. Replacing the
composite objective with a singleton-SPRT objective changes `L` from
`27.14048` to `28.22915`, so the proxy is rejected.

- [Raw two-sided sweep](../../evidence/claim5/raw_two_sided_sweep.csv)
- [Independent checker](../../evidence/claim5/independent_checker_output.json)
- [SPRT mutant](../../evidence/claim5/negative_control_output.json)
- [Limitations](../../evidence/claim5/limitations_and_deviations.md)
