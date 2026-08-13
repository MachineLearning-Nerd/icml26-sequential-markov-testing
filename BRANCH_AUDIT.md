# Branch audit

## Canonical surface

The canonical branch is `main`. It contains the integrated evidence,
producers, checkers, reports, and reproducibility runners. The remote cleanup
keeps only this branch; historical experiment branches are documented below
instead of remaining as ambiguous active variants.

## Historical branch roles

| Branch | Integrated responsibility |
| --- | --- |
| `orx/frozen-judged-baseline-certificate` | Preserved the judged baseline and immutable evidence. |
| `orx/faithful-core-contracts-and-algorithm-1` | Added the faithful composite core and initial contracts. |
| `orx/c1-c2-exact-lower-bound-and-poisson-certificates` | Strengthened C1/C2 exact and proof certificates. |
| `orx/c1-c2-lean-universal-proof-certificates` | Added formal Lean-oriented C1/C2 proof checks. |
| `orx/c3-exhaustive-dual-scale-algorithm-1-audit` | Added the exhaustive C3 clean-room audit. |
| `orx/c4-c5-proof-certified-asymptotic-campaign` | Added C4/C5 proof certificates and asymptotic campaigns. |
| `orx/paper-scale-mcmc-and-linear-mdp-applications` | Added paper-scale MCMC and linear-MDP evidence. |
| `orx/corrected-paper-scale-application-evidence` | Integrated corrected C6 application evidence. |
| `orx/hf-cpu-rerun-and-inline-claim-code` | Mirrored executable claim code for CPU reruns. |
| `orx/judge-visible-executable-claim-evidence` | Added judge-visible claim pages and the verifier. |
| `orx/hf-release-provenance-and-approval-gate` | Added release provenance and approval-gate checks. |
| `orx/release-candidate-report-and-protected-logbook` | Assembled the release report and protected logbook. |

These branches describe development lineage. They are not independent
scientific results and their raw `VERIFIED` labels are contract-level
labels only.

## Publication-time checks

- Repository: `icml26-sequential-markov-testing`.
- Default branch: `main`.
- Maintainer identity: MachineLearning-Nerd.
- Historical branch cleanup: recorded after the canonical main was published.
- Paper source: arXiv:2602.17587v3, OpenReview: YEckWPoS09.
