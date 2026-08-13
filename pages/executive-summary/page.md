# Executive summary

---
<!-- trackio-cell
{"type":"markdown","id":"cell_exec_summary_260217587","created_at":"2026-08-01T00:00:00+00:00","title":"Executive summary","pinned":true,"pinned_at":"2026-08-01T00:00:01+00:00"}
-->
**Six finite claim contracts pass on CPU; 0/6 paper-level claims are
independently verified; overall status is INCONCLUSIVE.** The historical judged
baseline remains **7/12** at Space revision
`d9bd4a1dbdcefc5ae653cca2b6d0f5b7b324237a`: Claim 6 was VERIFIED and Claims
1–5 were TOY. This candidate replaces the earlier known-alternative SPRT
proxies with the paper's composite Algorithm 1, exact finite certificates,
independent checkers, and mutation tests. These are finite contract results,
not a predicted judge score or a paper-level proof.

## Scope & cost

|  | This reproduction | Paper claim scope |
| --- | --- | --- |
| Scope | Theorems 3.3, 4.1, 4.4; Proposition 3.1; Algorithm 1; both Section 5 applications | All six selected claims |
| Hardware | Hugging Face `cpu-upgrade`, 8 vCPU; no accelerator | No GPU is needed for these checks |
| Compute | Exact certificates, exhaustive prefixes, 4,000 calibration/null paths, asymptotic sweeps, and 100,000-transition MDP runs | Universal statements retain proof audits; finite experiments are not substituted for quantifiers |
| Cost through canonical gate | 3h16m03s of CPU Jobs, approximately $0.098025 | Final format-regression rerun reported separately before publication |
| Outcome | Finite contracts: C1–C6 pass; paper-level: 0/6; overall: INCONCLUSIVE | Historical judge: 7/12; no new score claimed |

Links: [Hugging Face Space](https://huggingface.co/spaces/DineshAI/YEckWPoS09),
[canonical CPU Job](https://huggingface.co/jobs/DineshAI/6a6d255b6b79c09949c1dc58),
and [GitHub repository](https://github.com/MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing).

---
<!-- trackio-cell
{"type":"figure","id":"cell_reproduction_poster_260217587","created_at":"2026-08-01T00:00:02+00:00","title":"Reproduction poster (poster_embed.html)","poster":true,"pinned":true,"pinned_at":"2026-08-01T00:00:03+00:00"}
-->
<!-- poster_embed.html -->
<iframe src="poster_embed.html" title="Sequential Markov testing reproduction poster" width="100%" height="820" loading="lazy"></iframe>
