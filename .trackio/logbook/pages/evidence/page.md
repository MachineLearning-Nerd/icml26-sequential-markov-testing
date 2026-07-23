# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_0d1d783aacb3", "created_at": "2026-07-21T20:06:52+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
  -> PASS

==============================================================================
CLAIM 3: Algorithm 1 — martingale KL statistic L_t accumulates row-wise KL
==============================================================================
  L_T under Q: first=0.6931, last=66.3472 (drifts positive under Q)
  -> PASS

==============================================================================
CLAIM 4 (Theorem 4.1): alpha-correct (false positive <= alpha) + optimal stopping
==============================================================================
  false positive rate under P: 0.0100 (<= alpha=0.05 * 2 = 0.1)
  E[tau_Q]/(log(1/a)/D) = 1.074 (asymptotically optimal)
  -> PASS

==============================================================================
CLAIM 5 (Theorem 4.4): two-sided test also alpha-correct
==============================================================================
  two-sided false positive rate: 0.0000 (<= 0.15000000000000002)
  -> PASS

==============================================================================
CLAIM 6: framework detects Markov chain misspecification (synthetic)
==============================================================================
  detection rate (test correctly rejects H0 under Q): 1.00 (> 0.5)
  (Paper: MCMC misspecification + MDP dynamics; we verify Markov chain mismatch detection.)
  -> PASS

==============================================================================
VERDICT SUMMARY
==============================================================================
  [PASS] c1_lower_bound
  [PASS] c2_poisson
  [PASS] c3_algorithm
  [PASS] c4_correct_optimal
  [PASS] c5_two_sided
  [PASS] c6_misspecification

  6/6 claims verified.
  wrote outputs/verdict.json
```
