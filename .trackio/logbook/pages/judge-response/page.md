# Current executable evidence — response to the 5/12 verdict

**Status: published and awaiting a new live judge verdict.**

The 5/12 judge evaluated Space revision
`66d5e67b5426622768e4d797656e409526f3a299`. It could read the faithful result
pages and raw outputs, but that revision did not contain the Python that
generated them. The only executable snippets visible to the judge were the
archived small-chain SPRT checks, so it reasonably treated the new numerical
claims as unsupported.

This additive repair exposes the faithful implementation and an executable
independent checker without deleting the archived evidence:

The complete evidence bundle was published in revision
`c9f4f905993eda348b395b80ea9aac9447f5a170`. This publication status does not
predict a score; the last live verdict remains 5/12.

```text
uv run --python 3.12 --with numpy==2.3.3 --with scipy==1.16.2 python verify_candidate.py
```

The checker exits nonzero on a mismatch and reports `VERIFIED` only when every
claim-specific recomputation passes.

| Claim | Producing code | Independent executable check | Raw result |
| --- | --- | --- | --- |
| C1 full Theorem 3.3 correction | [`run_claim1`](../../candidate_code/run_core_campaign.py) and [`poisson_bound`](../../candidate_code/markov_core.py) | [`verify_claim1`](../../verify_candidate.py) | [`raw_lower_bound.csv`](../../evidence/claim1/raw_lower_bound.csv) |
| C2 actual Poisson operator bound | [`poisson_operator` / `poisson_bound`](../../candidate_code/markov_core.py) | [`verify_claim2`](../../verify_candidate.py) | [`raw_poisson_bounds.csv`](../../evidence/claim2/raw_poisson_bounds.csv) |
| C3 empirical kernel, composite GLR, and adaptive boundary | [`ThetaFamily.glr` / `simulate_test`](../../candidate_code/markov_core.py) | [`verify_claim3`](../../verify_candidate.py) | [`raw_trace.json`](../../evidence/claim3/raw_trace.json) |
| C4 composite Algorithm 1 alpha/optimality sweep | [`run_claim4`](../../candidate_code/run_core_campaign.py) | [`verify_claim4`](../../verify_candidate.py) | [`raw_alpha_sweep.csv`](../../evidence/claim4/raw_alpha_sweep.csv) |
| C5 two parallel composite GLRs | [`run_claim5`](../../candidate_code/run_core_campaign.py) | [`verify_claim5`](../../verify_candidate.py) | [`raw_two_sided_sweep.csv`](../../evidence/claim5/raw_two_sided_sweep.csv) |
| C6 Appendix-G MCMC and MountainCar | [`run_mcmc` / `run_mdp`](../../candidate_code/run_applications.py) | [`verify_claim6`](../../verify_candidate.py) | [`raw_mcmc.json`](../../evidence/claim6/raw_mcmc.json), [`raw_mdp.csv`](../../evidence/claim6/raw_mdp.csv) |

The archived baseline pages remain reachable and are now explicitly labelled
as superseded SPRT proxies. They are historical evidence, not the basis for the
current C1–C6 verdicts.
