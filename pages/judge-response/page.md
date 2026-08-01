# Current executable evidence — response to the 7/12 verdict

**Status: strengthening candidate, not yet published or re-judged.**

The live judge evaluated Space revision `d9bd4a1dbdcefc5ae653cca2b6d0f5b7b324237a` and awarded 7/12: Claim 6 is VERIFIED, while Claims 1–5 remain TOY. The strengthened evidence passed on [Hugging Face `cpu-upgrade` Job `6a6d0d14a00abefd4b28a381`](https://huggingface.co/jobs/DineshAI/6a6d0d14a00abefd4b28a381) at commit `c5980d250d89368030c5ce9c160583e7f4d83460`, using CPU only. No score increase is claimed before publication and a new verdict.

The candidate addresses each remaining criticism directly:

| Claim | Prior issue | Replacement evidence |
| --- | --- | --- |
| C1 | One five-state test cannot establish a universal lower bound | Exact LR-hitting family with `E[tau]=5k-1`, exact Poisson endpoint correction, 1,354 rational stopped-Wald identities, complete proof-dependency certificate, and an exact counterexample to dropping the correction |
| C2 | Four two-state cells are too narrow | 66 dense/sticky/cyclic/reversible/skewed/iid cells through 50 states, certified pseudo-gap maxima, actual Poisson operators, attaining sign witnesses, and an explicit repair of the source proof's `n=0` domain gap |
| C3 | One five-state Algorithm 1 trace | All 9,837 path prefixes through depth seven plus 81 dense/sticky/cyclic checkpoints through 50 states, checked by clean-room code; five component mutants fail |
| C4 | 200 null trials and ratios still far from `1/D_inf` | Exact infinite-horizon mixture/e-process certificate, 2,000 broad null paths, 128 paths per asymptotic cell through log threshold 5,120, and 150 stationary-flow limit cells through `1e8`; worst final upper ratio `1.02993` |
| C5 | Only 90 trials | Faithful parallel composite GLRs under both truths, three joint approach rates, 128 paths per asymptotic cell, 2,000 calibration paths, both full Bernoulli-KL/Poisson lower bounds, exact event inclusion, zero asymptotic decision errors, and worst final upper ratio `1.04179` |
| C6 | — | Previously VERIFIED evidence is retained and rerun unchanged |

The Space-root checker independently reloads raw outputs and exits nonzero on any failed contract. It rejects known-alternative SPRTs for C4, Bonferroni proxies for C5, self-reported Poisson constants without actual operator witnesses, and any missing adaptive-boundary component.

```text
uv run --python 3.12 --with numpy==2.3.3 --with scipy==1.16.2 python verify_candidate.py
```

All files from every judged revision remain protected. Candidate evidence is additive; archived SPRT pages remain reachable as historical evidence only.
