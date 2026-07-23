# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_b1bb7b8a590f", "created_at": "2026-07-21T20:06:50+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Theorem 3.3 gives a non-asymptotic instance-dependent lower bound on the expected stopping time, E_Q[tau_alpha] ≥ (log(1/alpha)/D_M^inf(Q,P) − 2C_Q/min_i pi_i)^+, where D_M^inf(Q,P) is a stationary-weighted projection distance and C_Q bounds a Poisson-equation solution (Theorem 3.3).
2. Proposition 3.1 bounds the Poisson-equation solution constant C_Q via the pseudo-spectral gap of the underlying Markov chain (Section 3, Proposition 3.1).
3. The proposed Sequential Markov Chain Test (Algorithm 1) builds an empirical transition kernel and a martingale statistic L_t accumulating row-wise KL divergences from the null class, stopping when L_t exceeds an adaptive boundary beta_t (Section 4, Algorithm 1).
4. Theorem 4.1 proves the proposed test is alpha-correct and asymptotically optimal, with limsup_{alpha->0} E_Q[tau_alpha]/log(1/alpha) ≤ 1/D_M^inf(Q,P), matching the Theorem 3.3 lower bound (Theorem 4.1).
5. Theorem 4.4 extends the one-sided asymptotic optimality result to the two-sided testing setting (Section 4.2, Theorem 4.4).
6. The framework is applied to detect MCMC transition-kernel misspecification (Section 5.1, Corollary 5.1) and to validate linear transition dynamics in MDPs (Section 5.2, Corollary 5.3).
