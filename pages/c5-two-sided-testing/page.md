# C5 — two-sided composite test

**Finite contract status: PASS. Paper-level status: not independently verified.**

This is Theorem 4.4's construction: two non-singleton composite Algorithm 1
tests run on the same path, stopping at their minimum with the paper's tie
rule. There is no Bonferroni split and no known-alternative SPRT.

The asymptotic campaign uses 128 independent paths under each truth. It checks
five base thresholds through 5,120 along three joint approaches
`log(1/beta)/log(1/alpha)=0.5,1,2`. Under `Q`, stopping time is normalized by
`log(1/alpha)` and compared with `1/D_M^inf(Q,P)`; under `P`, it is normalized
by `log(1/beta)` and compared with `1/D_M^inf(P,Q)`. Every largest-threshold
one-sided 95% upper bound must be at most 1.10 times its direction-specific
target.
The accepted CPU run has zero asymptotic decision errors and a worst final
direction-specific upper ratio of `1.0417864936`.

Both full non-asymptotic lower bounds are also evaluated, including the stable
Bernoulli-KL terms and `2 C / pi_min` Poisson corrections. The sample-mean
lower confidence bound must exceed the paper bound in every cell, with a
non-vacuous bound under each truth.

Correctness is not inferred from zero errors alone. The exact event inclusions

`{wrong under P} subset {the P-null test stops}` and
`{wrong under Q} subset {the Q-null test stops}`

combine with the Claim 4 e-process certificate to prove the level
`(alpha,beta)` guarantee. Separately, 1,000 independent calibration paths per
truth at three practical error pairs must have exact one-sided binomial upper
bounds below the applicable alpha or beta.

Mutants replacing the minimum by a maximum, using the wrong normalizer under
`P`, or swapping the directional information projections are all required to
fail. The source audit also records harmless appendix symbol/index typos while
retaining the theorem statement's exact quantifiers.

- [Claim contract](../../evidence/claim5_v2/claim_contract.json)
- [Accepted Hugging Face CPU run](../../evidence/claim5_v2/accepted_run.json)
- [Joint-limit summaries](../../evidence/claim5_v2/raw_summary.csv)
- [Raw shared-path trials](../../evidence/claim5_v2/raw_trials.csv)
- [Calibration summaries](../../evidence/claim5_v2/raw_calibration_summary.csv)
- [Full stationary-flow matrix](../../evidence/claim5_v2/raw_stationary_flow_matrix.csv)
- [Proof obligations](../../evidence/claim5_v2/proof_certificate.json)
- [Independent checker](../../evidence/claim5_v2/independent_checker_output.json)
- [Failing mutants](../../evidence/claim5_v2/negative_control_output.json)
- [Complete producer](../../candidate_code/run_claim45_v2.py)
- [Complete judge-visible verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim5_v2/limitations_and_deviations.md)
