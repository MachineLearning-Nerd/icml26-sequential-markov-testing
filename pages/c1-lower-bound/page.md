# C1 — full Theorem 3.3 lower bound

**Candidate evidence verdict: VERIFIED. Live judged baseline: TOY until this candidate is published and judged.**

The old page checked one five-state test and could not establish a theorem quantified over every alpha-correct power-one stopping time. The replacement separates an exact witness family from the universal proof certificate.

For

\[
Q=\begin{pmatrix}1/3&2/3\\1&0\end{pmatrix},\qquad
P=\begin{pmatrix}2/3&1/3\\1&0\end{pmatrix},
\]

the threshold-`k log 2` likelihood-ratio test has exact Type-I error `2^-k`, power one, stationary information `(log 2)/5`, and expected stopping time `5k-1`. Its endpoint Poisson correction is exactly `(log 2)/5`, so it attains Theorem 3.3's first inequality:

\[
\mathbb E_Q\tau=5k-1
=\frac{\log(1/\alpha)}{D_M(Q,P)}
-\frac{\mathbb E[\omega(X_0)-\omega(X_\tau)]}{D_M(Q,P)}.
\]

This also rigorously rejects the old leading-only proxy: `5k-1 < 5k` for every tested `k`. Exact rational arithmetic checks the stationary law, Poisson equation, gambler's-ruin error probability, stopping-time recurrence, and all 1,354 bounded stopping policies through depth four.

The theorem-wide certificate audits the complete implication chain: stopped-path data processing, the stopped Wald-Poisson identity, `||omega|| <= C_Q ||f||`, `D_M >= pi_min ||f||`, optimization over every null member, and the positive part. The finite witness is not presented as proof of the universal quantifier.

- [Claim contract](../../evidence/claim1_v2/claim_contract.json)
- [Accepted Hugging Face CPU run](../../evidence/claim1_v2/accepted_run.json)
- [Exact raw test family](../../evidence/claim1_v2/raw_exact_test_family.csv)
- [Proof certificate](../../evidence/claim1_v2/proof_certificate.json)
- [Independent checker](../../evidence/claim1_v2/independent_checker_output.json)
- [Negative controls](../../evidence/claim1_v2/negative_control_output.json)
- [Evaluation](../../evidence/claim1_v2/EVAL.md)
- [Producer](../../candidate_code/run_claim12_v2.py)
- [Independent verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim1_v2/limitations_and_deviations.md)
