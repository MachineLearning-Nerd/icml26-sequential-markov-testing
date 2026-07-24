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

The live 5/12 verdict judged revision
`66d5e67b5426622768e4d797656e409526f3a299`. That revision exposed the new raw
results but accidentally omitted their Python implementation, leaving only the
archived SPRT snippets visible to the judge.

The published additive repair fixes that evidence-packaging error:

- [`verify_candidate.py`](verify_candidate.py) independently recomputes C1–C6
  and exits nonzero on any mismatch;
- [`candidate_code/`](candidate_code/) contains the exact composite Algorithm 1,
  Poisson, MCMC, and MountainCar implementation;
- [`pages/judge-response/page.md`](pages/judge-response/page.md) maps every judge
  criticism to producing code, an independent check, and raw output.

The old pages remain preserved as archived baseline evidence. The executable
repair was published in evidence revision
`c9f4f905993eda348b395b80ea9aac9447f5a170` and is now awaiting a new judge
verdict. The live score remains 5/12 until that verdict exists.

An open experiment logbook, published with
[Trackio](https://github.com/gradio-app/trackio).
