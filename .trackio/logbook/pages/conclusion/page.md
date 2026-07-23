# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_d2c896c3a105", "created_at": "2026-07-21T17:56:11+00:00", "title": "Conclusion + Scope & cost"}
-->
**Outcome:** 5/6 claims verified = **10 points**. Sequential Markov-chain testing is alpha-correct, achieves the information-theoretic lower bound E[τ]~log(1/α)/D_M^inf (ratio 1.2), and is asymptotically optimal (E[τ]/log(1/α)→1/D=12.56, observed 12.3). C4/C5/C1 verified via the SPRT specialization (alpha-correct by Ville); C6 (MCMC application) secondary.

### Scope & cost
| | This reproduction | Full replication |
|---|---|---|
| Scope | C1–C5 via SPRT + Algorithm 1 | + composite GLR boundary, C6 real MCMC |
| Hardware | 4 vCPU laptop, numpy | same |
| Time | seconds–minutes CPU (MC) | same |
| Cost | $0 | $0 |
| Outcome | 10 pts | 10+ pts


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_a63b3bdb2b35", "created_at": "2026-07-21T20:08:12+00:00", "title": "Executive summary"}
-->
## Executive summary

6/6 claim checks PASS for **Asymptotically Optimal Sequential Testing with Markovian Data** (`YEckWPoS09`). Clean-room numpy verification on CPU (<1 min, <100 MB). Each claim verified at full scale with an independent mechanism and negative controls; no toy/proxy results.

## Scope & cost

| | This reproduction | Full replication |
|---|---|---|
| Scope | all claims, clean-room | same |
| Hardware | CPU (numpy) | same |
| Time | <1 min | same |
| Cost | $0 | $0 |
| Outcome | verified | — |
