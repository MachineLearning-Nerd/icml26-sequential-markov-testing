# C3 — exhaustive dual-scale Algorithm 1 audit

**Finite contract status: PASS. Paper-level status: not independently verified.**

The new audit checks Algorithm 1 at two complementary scales. It exhaustively
enumerates every one of the 9,837 path prefixes through seven transitions from
all initial states of a positive three-state family. It then checks deterministic
paths for dense, sticky, and cyclic positive kernels with 5, 10, 25, and 50
states.

[`claim3_cleanroom.py`](../../candidate_code/claim3_cleanroom.py) imports no
production Markov-testing code. It reconstructs the tilted kernel with an
independent power-method Perron solver, computes every row-wise weighted KL term
directly, optimizes the continuous composite null, and evaluates the adaptive
boundary. [`verify_claim3`](../../verify_candidate.py) fails unless all
exhaustive cases and all 81 multi-scale checkpoints match.

The implementation being checked follows Algorithm 1 rather than a
known-alternative SPRT:

```python
counts[state, next_state] += 1
visits = counts.sum(axis=1)
empirical = empirical_log_likelihood(counts)
null_ll = np.max(np.einsum("gij,ij->g", family.log_kernels, counts))
L_t = max(0.0, empirical - null_ll)
psi_t = np.log(math.e * (1.0 + visits / (m - 1))).sum()
beta_t = math.log(1 / alpha) + (m - 1) * psi_t
if L_t >= beta_t:
    return stopping_time
```

The audit separately mutates each defining component: unvisited-row
initialization, row-visit weighting, composite projection, adaptive `psi_t`, and
the `(m-1)` multiplier. Every mutant must be rejected. Both stopping and
continuation decisions must occur in the exhaustive set.

Across the accepted run, the maximum production/clean-room statistic error is
`3.7801e-12`, the maximum boundary error is `4.5475e-13`, and the empirical
kernel error is exactly zero.

The representative five-state trace remains available and stops at transition
93. The larger audit is explicitly structural: it does not claim to prove the
alpha-correctness or asymptotic-optimality results in Theorem 4.1.

- [Strengthened claim contract](../../evidence/claim3_v2/claim_contract.json)
- [Accepted Hugging Face CPU run](../../evidence/claim3_v2/accepted_run.json)
- [Exhaustive summary](../../evidence/claim3_v2/raw_exhaustive_summary.json)
- [Every unique exhaustive count table](../../evidence/claim3_v2/raw_exhaustive_table.csv)
- [Multi-scale raw matrix](../../evidence/claim3_v2/raw_dimension_matrix.csv)
- [Representative raw trace](../../evidence/claim3_v2/raw_trace.json)
- [Independent checker](../../evidence/claim3_v2/independent_checker_output.json)
- [Five negative controls](../../evidence/claim3_v2/negative_control_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
- [Complete Algorithm 1 implementation](../../candidate_code/markov_core.py)
- [Clean-room implementation](../../candidate_code/claim3_cleanroom.py)
- [Complete independent verifier](../../verify_candidate.py)

The previously judged C3 files remain preserved under
[`evidence/claim3`](../../evidence/claim3/); they are historical evidence, not
removed or overwritten.
