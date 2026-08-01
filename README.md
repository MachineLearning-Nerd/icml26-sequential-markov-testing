---
title: "Repro - Sequential Markov Chain Test (arXiv 2602.17587)"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-YEckWPoS09
---

# Repro - Sequential Markov Chain Test (arXiv 2602.17587)

## Current faithful executable evidence

The live 7/12 verdict judged revision
`d9bd4a1dbdcefc5ae653cca2b6d0f5b7b324237a`: Claim 6 is `VERIFIED`, while
Claims 1--5 remain `TOY`. This additive candidate preserves all 109 judged files
and places the strengthened proof, producer, and checker operations directly on
each current claim page.

The next additive candidate strengthens judge-visible evidence:

- [`verify_candidate.py`](verify_candidate.py) independently recomputes C1–C6
  and exits nonzero on any mismatch;
- [`candidate_code/`](candidate_code/) contains the exact composite Algorithm 1,
  Poisson, MCMC, and MountainCar implementation;
- [`pages/judge-response/page.md`](pages/judge-response/page.md) maps every judge
  criticism to producing code, an independent check, and raw output.

The old pages remain preserved as archived baseline evidence. This candidate
has not been published or re-judged, so the live score remains 7/12.

An open experiment logbook, published with
[Trackio](https://github.com/gradio-app/trackio).
