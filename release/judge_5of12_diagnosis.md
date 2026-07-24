# Live 5/12 verdict diagnosis

- Verdict dataset revision inspected: `a6eb7d81d421853d0f15308fb96855266c2b269f`
- Filter used: `space_id == "DineshAI/YEckWPoS09"`
- Judged Space revision: `66d5e67b5426622768e4d797656e409526f3a299`
- Judged at: `2026-07-23T16:36:19+00:00`
- Score: `5/12`
- Verdicts: C1 TOY, C2 INCONCLUSIVE, C3 TOY, C4 TOY, C5 TOY, C6 TOY

## Root cause

The judge evaluated the intended Space revision. The revision contained 99
files, including the new raw evidence and current pages, but no `.py` files.
The current pages described stronger results without exposing the implementation
that produced them. The only executable snippets visible to the judge were the
preserved baseline SPRT proxies, so it could not distinguish the faithful
campaign from unsupported narrative.

## Claim-level reasons and repair

| Claim | Why credit was withheld | Executable repair |
|---|---|---|
| C1 | Full correction was described but no code produced \(D^\inf_M\), \(C_Q\), \(\pi_{\min}\), and the bound | Recompute all four quantities and both vacuous/non-vacuous cells from raw evidence |
| C2 | Actual Poisson norms and pseudo-gaps were described but not executable | Recompute four Poisson operator norms and analytic pseudo-gaps independently |
| C3 | Visible code was only a small sanity run or SPRT | Rebuild every empirical row, continuous composite projection, row-wise KL statistic, adaptive boundary, and stopping event |
| C4 | Visible code used a known-alternative SPRT; 0/200 and the threshold sweep lacked visible backing | Require the composite `simulate_test`, five thresholds, 20 trials each, null rotation, and Clopper–Pearson bound; reject `sequential_lr_test` |
| C5 | Visible code was Bonferroni-split SPRTs | Require two composite GLR directions, direction-specific coefficients, 90 trials, and a singleton-objective mutant |
| C6 | MCMC and MountainCar numbers lacked visible application code | Require the exact five-state MCMC setup, the MountainCar generator, 100+100 MCMC runs, 20×3 100k-transition MDP rows, null controls, and independent solver checks |

The candidate Space now adds five byte-identical source files under
`candidate_code/`, a root `verify_candidate.py`, per-claim code/output links,
and `evidence/judge_visible_verifier.json`. It preserves all 99 paths from the
5/12 revision and all 21 paths from the original judged revision.

This diagnosis does not predict a future score. Only a new live judge verdict
can assign credit after publication.
