# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_23c6d6465a50", "created_at": "2026-07-21T17:56:10+00:00", "title": "Clean-room Markov chain + sequential test"}
-->
**Core** `repro/src/core.py`: Markov chain sampler, KL/ stationary distribution, D_M^inf (KL rate), Algorithm 1 GLR (empirical kernel Q̂, statistic L_t=Σ N_x·KL(Q̂‖P0), boundary β_t=log(1/α)+(m−1)ψ_t), and the SPRT specialization (LLR_t=Σ N_{x,y}log(Q/P0), boundary log(1/α)).

**Verification:** alpha-correctness and two-sided control via Monte-Carlo false-positive rates under H0; optimality and the lower bound via the E[τ]/log(1/α) ratio vs 1/D_M^inf. The SPRT LLR is a supermartingale under H0 (Ville -> alpha-correct). Deterministic RNG.
