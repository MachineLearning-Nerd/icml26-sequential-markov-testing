# C2 — Proposition 3.1 Poisson control

**Finite contract status: PASS. Paper-level status: not independently verified.**

The old evidence only checked four two-state chains. The replacement computes the actual centered Poisson operator, its induced infinity norm, and an attaining sign-vector witness in 66 cells: dense, sticky, cyclic, reversible, skewed, and i.i.d.-corner kernels in 2, 3, 5, 10, 25, and 50 states.

For every non-i.i.d. cell, the checker evaluates

\[
\gamma_{\rm ps}=\max_{k\ge1}\frac{\gamma((P^*)^kP^k)}{k}
\]

until `1/(k+1)` is below the incumbent, certifying that no untested `k` can improve the maximum. It independently solves the Poisson operator and requires

\[
\| (I-P+\mathbf1\pi)^{-1}(I-\mathbf1\pi)\|_{\infty\to\infty}\le C_P.
\]

The source proof cites Paulin's mixing inequality for `n>=1` but applies it to a series beginning at `n=0`. The candidate records and repairs this domain gap explicitly: the zeroth row contribution is `2(1-pi_x)||f||`, it fits inside the published envelope, and Paulin is summed only from one. The proposition and its constant are unchanged. Six identical-row kernels separately verify the `gamma_ps=1, C_P=2` branch.

This is not the prior tautology that an invented `1/gap` value is finite: every row contains the actual Poisson norm, a norm-attaining witness, the exact paper constant, and the certified pseudo-gap search.
The largest actual-norm/published-bound ratio is `0.9997614502`, so the
campaign includes a near-tight cell rather than only loose easy cases.

- [Claim contract](../../evidence/claim2_v2/claim_contract.json)
- [Accepted Hugging Face CPU run](../../evidence/claim2_v2/accepted_run.json)
- [Raw 66-cell matrix](../../evidence/claim2_v2/raw_poisson_matrix.csv)
- [Proof and source-repair certificate](../../evidence/claim2_v2/proof_certificate.json)
- [Independent checker](../../evidence/claim2_v2/independent_checker_output.json)
- [Negative controls](../../evidence/claim2_v2/negative_control_output.json)
- [Evaluation](../../evidence/claim2_v2/EVAL.md)
- [Producer](../../candidate_code/run_claim12_v2.py)
- [Independent verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim2_v2/limitations_and_deviations.md)
