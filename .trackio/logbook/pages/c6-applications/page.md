# C6 — MCMC and linear-MDP applications

**Verdict: VERIFIED**

**Executable evidence.** [`run_mcmc` and
`run_mdp`](../../candidate_code/run_applications.py) expose the exact
five-state stationary-null projection, Gymnasium `MountainCar-v0`, 8×8 grid,
three actions, 20 paths, 100,000 transitions, and `d=3,5,7`.
[`verify_claim6`](../../verify_candidate.py) checks the code and every raw trial
count, solver comparison, detection rate, and null control; see its
[`precomputed output`](../../evidence/judge_visible_verifier.json).

Both named applications are reproduced.

For MCMC, the exact Appendix-G five-state target and matrices give
`100/100` detections under misspecification and `0/100` rejections for a
kernel with the correct stationary law. Mean misspecified stopping time is
`2472.0` transitions (SD `398.566`). Independent convex solvers agree to
`3.38e-7` relative error.

For MountainCar, the reported 8×8 state grid, three actions, twenty
100,000-transition paths, and feature dimensions `d=3,5,7` give mean final
statistics `255267.6, 241507.8, 197174.9` and rejection rates
`100%, 100%, 85%`. There are exactly twenty final rows per dimension. All
three exact linear-null controls remain below boundary. CLARABEL agrees with
an independent analytic-gradient SciPy simplex optimizer to `4.28e-8`
relative error.

The source omits the RBF bandwidth and seeds; this reproduction pins
`sigma=32` and seed `260217587` and labels them as substitutions.

- [Raw MCMC runs](../../evidence/claim6/raw_mcmc.json)
- [Raw MDP rows](../../evidence/claim6/raw_mdp.csv)
- [Independent solvers](../../evidence/claim6/independent_checker_output.json)
- [Null controls](../../evidence/claim6/negative_control_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
- [Limitations](../../evidence/claim6/limitations_and_deviations.md)
