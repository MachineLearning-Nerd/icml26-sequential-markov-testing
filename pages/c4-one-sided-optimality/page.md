# C4 — one-sided alpha control and optimality

**Candidate verdict: VERIFIED. Live judge verdict remains TOY until this
candidate is published and judged.**

This candidate tests Theorem 4.1 itself: the composite Algorithm 1 GLR, its
adaptive `psi_t` boundary, infinite-horizon alpha control, and the coefficient
`1/D_M^inf`. It does not substitute a known-alternative SPRT.

The stochastic campaign exceeds the paper's reported 100-epoch synthetic
protocol. For each of `theta=-0.8,-0.6,-0.4`, it uses 128 independent paths at
`log(1/alpha)=320,640,1280,2560,5120`. A result is accepted only if the
one-sided 95% upper confidence bound at 5,120 is at most `1.10 / D_M^inf` for
every alternative. The old “moves closer” criterion is gone.
The accepted CPU run's worst final upper ratio is `1.0299323977`, below the
predeclared `1.10` limit.

Alpha control has two independent layers:

- 2,000 finite-horizon null paths span 21 null parameters and every initial
  state at `alpha=0.05` and `0.01`; exact one-sided Clopper–Pearson bounds must
  be below the corresponding alpha.
- An executable normalized-Dirichlet mixture certificate proves the exact
  conditional martingale identity and its domination of
  `exp(L_t-(m-1)psi_t)`. Together with the composite-infimum event inclusion
  and Ville's inequality, this addresses all times and all alpha, not only the
  Monte Carlo horizon.

The first-order coefficient is additionally checked on deterministic
stationary flows for dense, sticky, and cyclic positive kernels in
3/5/10/25/50 states, through log threshold `1e8`. Removing `psi_t` and scaling
`log(1/alpha)` by 1.2 are required to fail.

The source says the mixture prior is `Dir(1,...,1)`, but one displayed integral
contains an extra `prod q_i` inconsistent with that named prior and with every
following Gamma/factorial line. The certificate uses the normalized uniform
Dirichlet density matching the stated prior and subsequent derivation, and
records this transcription issue explicitly.

- [Claim contract](../../evidence/claim4_v2/claim_contract.json)
- [Accepted Hugging Face CPU run](../../evidence/claim4_v2/accepted_run.json)
- [128-path asymptotic summaries](../../evidence/claim4_v2/raw_summary.csv)
- [Raw alternative paths](../../evidence/claim4_v2/raw_trials.csv)
- [2,000-path null summaries](../../evidence/claim4_v2/raw_null_summary.csv)
- [Exact mixture count certificate](../../evidence/claim4_v2/raw_mixture_certificate.csv)
- [Multi-scale stationary-flow matrix](../../evidence/claim4_v2/raw_stationary_flow_matrix.csv)
- [Proof obligations](../../evidence/claim4_v2/proof_certificate.json)
- [Independent checker](../../evidence/claim4_v2/independent_checker_output.json)
- [Failing mutants](../../evidence/claim4_v2/negative_control_output.json)
- [Complete producer](../../candidate_code/run_claim45_v2.py)
- [Complete judge-visible verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim4_v2/limitations_and_deviations.md)
