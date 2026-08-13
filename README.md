---
title: "ICML 2026 — Sequential Testing with Markovian Data"
emoji: "🎯"
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
  - icml2026-repro
  - paper-YEckWPoS09
  - source-pinned
  - finite-audit
---

# ICML 2026 — Sequential Testing with Markovian Data

Independent, CPU-only, source-pinned audit for:

> Alhad Sethi, Kavali Sofia Sagar, Shubhada Agrawal, Debabrota Basu, and P. N. Karthik.
> “Asymptotically Optimal Sequential Testing with Markovian Data.”
> ICML 2026. [arXiv:2602.17587v3](https://arxiv.org/abs/2602.17587v3).
> OpenReview: [YEckWPoS09](https://openreview.net/forum?id=YEckWPoS09).

Repository name: `icml26-sequential-markov-testing`

## Current status

**Overall: INCONCLUSIVE.** The repository contains six reproducible finite
claim contracts, and all six finite contracts pass. That is different from
independently proving the paper’s universal, asymptotic, or alpha-correctness
claims.

| Layer | Result | Meaning |
| --- | --- | --- |
| Finite contract checks | 6/6 pass | The declared source-pinned inputs, invariants, certificates, numerical checks, and negative controls pass. |
| Paper-level claims | 0/6 independently verified | The finite audit does not establish universal quantifiers, infinite-horizon guarantees, or limiting equalities. |
| Consolidated status | INCONCLUSIVE | Evidence is useful and reproducible, but it is not a paper-level verification. |

The raw files under `outputs/` and `evidence/` retain the
producer vocabulary `VERIFIED`. In those files it means that a finite
contract passed. The consolidated gate in `publication_gate.json`
deliberately reports the stronger paper-level boundary above.

Historical Hugging Face judge results are preserved as provenance: 5/12 at
revision `66d5e67` and 7/12 at revision `d9bd4a1`. No new
judge score is inferred from the local finite checks.

## What the paper does

The paper studies sequential testing for Markov transition kernels when the
null is composite. Its construction uses an empirical transition kernel,
row-wise information projections onto the composite null, an adaptive
boundary, and two parallel tests for the two-sided problem. It also connects
the framework to MCMC misspecification and linear transition models in MDPs.

## Claim ledger: producer → evidence → interpretation

| Claim | Paper object | What produces the evidence | Finite result and boundary |
| --- | --- | --- | --- |
| C1 | Theorem 3.3 lower bound | `candidate_code/run_claim12_v2.py` → `evidence/claim1_v2/`; exact witnesses, Poisson endpoint correction, and 1,354 bounded stopping-policy identities | Finite contract pass; does not prove the theorem’s universal quantifier. |
| C2 | Proposition 3.1 Poisson control | `candidate_code/run_claim12_v2.py` → `evidence/claim2_v2/`; 66 kernel cells, actual Poisson operators, pseudo-gap search, and sign witnesses | Finite contract pass; does not prove the proposition for every admissible kernel. |
| C3 | Algorithm 1 | `candidate_code/claim3_cleanroom.py` and `verify_candidate.py` → `evidence/claim3_v2/`; 9,837 prefixes, 81 multi-scale checkpoints, and component mutants | Finite structural pass; does not prove alpha-correctness or asymptotic optimality. |
| C4 | Theorem 4.1 | `candidate_code/run_claim45_v2.py` → `evidence/claim4_v2/`; mixture certificate, null paths, asymptotic sweep, and stationary-flow checks | Finite contract pass; does not replace the universal martingale and limiting proof. |
| C5 | Theorem 4.4 | `candidate_code/run_claim45_v2.py` → `evidence/claim5_v2/`; two composite directions, joint-limit paths, calibration, lower bounds, and mutants | Finite contract pass; does not prove the two-sided theorem in the limit. |
| C6 | Corollaries 5.1 and 5.3 | `repro/src/run_applications.py` → application summaries; MCMC misspecification and linear-MDP runs with valid-null controls | Finite application pass; substitutions and limited checkpoints are documented. |

Every claim has a claim contract, raw output, producer, independent checker, and
limitations file. A claim is accepted locally only when its declared finite
checks pass and its failure-seeking controls detect the corresponding mutant.

## Reproduce

The full publication-gate command is:

```bash
uv sync --frozen && uv run python repro/src/run_publication_gate.py
```

This command regenerates the finite evidence and release checks. It does not
turn finite results into a proof of the paper. To verify the judge-visible
bundle without rerunning the long campaign:

```bash
uv run --python 3.12 --with numpy==2.3.3 --with scipy==1.16.2 python verify_candidate.py
```

The pinned local paper source has SHA-256:
`2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8`.

## Limitations and deviations

- Finite paths, cells, stopping policies, and thresholds cannot establish
  universal or asymptotic statements.
- The MDP reproduction fixes `sigma=32` and seed `260217587`;
  those values are substitutions because the paper does not provide them.
- The MDP run uses six durable checkpoints while generating the full transition
  trajectories.
- The C4 certificate follows the stated uniform Dirichlet prior where one
  displayed source integral appears inconsistent with that prior and its
  subsequent Gamma calculation. The deviation is recorded in the evidence.
- Historical Hugging Face pages and raw `VERIFIED` labels are retained
  for provenance, not presented as independent paper proof.

## Branches

`main` is the canonical publication surface. The following historical
`orx/*` branches were integrated into it and are documented here so
their roles are not lost:

| Historical branch | Role |
| --- | --- |
| `orx/frozen-judged-baseline-certificate` | Preserved the judged baseline and immutable evidence. |
| `orx/faithful-core-contracts-and-algorithm-1` | Added the faithful composite core and initial contracts. |
| `orx/c1-c2-exact-lower-bound-and-poisson-certificates` | Strengthened C1 and C2 exact/proof certificates. |
| `orx/c1-c2-lean-universal-proof-certificates` | Added formal Lean-oriented C1/C2 proof checks. |
| `orx/c3-exhaustive-dual-scale-algorithm-1-audit` | Added the C3 exhaustive clean-room audit. |
| `orx/c4-c5-proof-certified-asymptotic-campaign` | Added C4/C5 proof certificates and asymptotic campaigns. |
| `orx/paper-scale-mcmc-and-linear-mdp-applications` | Added the paper-scale C6 applications. |
| `orx/corrected-paper-scale-application-evidence` | Integrated the corrected application evidence. |
| `orx/hf-cpu-rerun-and-inline-claim-code` | Mirrored executable claim code for CPU reruns. |
| `orx/judge-visible-executable-claim-evidence` | Added judge-visible pages, producers, and verifier links. |
| `orx/hf-release-provenance-and-approval-gate` | Added release provenance and approval-gate checks. |
| `orx/release-candidate-report-and-protected-logbook` | Assembled the release report and protected logbook. |

The legacy branches are historical lineage, not separate supported variants.
The cleaned remote retains only `main`; see
[BRANCH_AUDIT.md](BRANCH_AUDIT.md) for the publication-time audit.

## Repository map

- `candidate_code/`: claim producers and clean-room checkers.
- `evidence/`: source-pinned contracts, raw outputs, certificates,
  negative controls, and limitations.
- `repro/src/`: the reproducibility runners and application checks.
- `pages/`: Trackio/Hugging Face evidence pages.
- `reports/`: the claim-by-claim narrative report.
- `outputs/`: raw verification and consolidated gate outputs.
- `source/`: the pinned paper source archive.
- `STATUS.md`, `GATE_READY.md`, and
  `BRANCH_AUDIT.md`: status, gate scope, and branch lineage.

## Citation

```bibtex
@inproceedings{sethi2026asymptotically,
  title     = {Asymptotically Optimal Sequential Testing with Markovian Data},
  author    = {Sethi, Alhad and Sagar, Kavali Sofia and Agrawal, Shubhada and Basu, Debabrota and Karthik, P. N.},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year      = {2026},
  url       = {https://arxiv.org/abs/2602.17587v3}
}
```

## Thank you and attribution

Thank you to Alhad Sethi, Kavali Sofia Sagar, Shubhada Agrawal, Debabrota Basu,
and P. N. Karthik for making the paper and its research direction available for
careful study. This repository is an independent reproduction/audit, not an
official implementation or endorsement by the authors.

Maintained by [MachineLearning-Nerd](https://github.com/MachineLearning-Nerd).
