# C5 — two-sided composite test

**Verdict: VERIFIED**

**Executable evidence.** [`run_claim5`](../../candidate_code/run_core_campaign.py)
executes `simulate_test` twice on each shared path with two non-singleton
`ThetaFamily` nulls. There is no Bonferroni split or known-alternative SPRT.
[`verify_claim5`](../../verify_candidate.py) checks the source structure, both
truth directions, 90 trial rows, and the singleton-SPRT mutant; see its
[`precomputed output`](../../evidence/judge_visible_verifier.json).

The implementation runs the two paper Algorithm 1 composite GLRs in parallel
and stops at their minimum; it does not use two Bonferroni-split,
known-alternative SPRTs.

Both generating sides are evaluated at three log thresholds with fifteen
trials per side and cell: 90 trials total, with zero decision errors. For both
directions, the largest-threshold normalized stopping ratio is closer to its
direction-specific `1/D_inf` coefficient than the first ratio. Replacing the
composite objective with a singleton-SPRT objective changes `L` from
`27.14048` to `28.22915`, so the proxy is rejected.

The two directions share each sampled path and each uses a non-singleton
composite family:

```python
forward = simulate_test(kernel, target_family, log_level, seed, 20_000, initial)
reverse = simulate_test(kernel, reverse_family, log_level, seed, 20_000, initial)
forward_time = forward["stopping_time"] or 10**12
reverse_time = reverse["stopping_time"] or 10**12
decision = truth if forward_time <= reverse_time else opposite_truth
errors += int(decision != truth)
stops.append(min(forward_time, reverse_time))
assert target_family.high > target_family.low
assert reverse_family.high > reverse_family.low
```

No Bonferroni split and no `sequential_lr_test` appear in the producing or
checking source.

- [Raw two-sided sweep](../../evidence/claim5/raw_two_sided_sweep.csv)
- [Independent checker](../../evidence/claim5/independent_checker_output.json)
- [SPRT mutant](../../evidence/claim5/negative_control_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
- [Complete two-sided producer](../../candidate_code/run_core_campaign.py)
- [Complete independent verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim5/limitations_and_deviations.md)
