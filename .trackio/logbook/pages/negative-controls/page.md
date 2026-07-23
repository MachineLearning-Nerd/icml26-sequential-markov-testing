# Candidate negative controls

Every faithful verifier has a failure-seeking control:

| Claim | Mutant or valid-null control | Result |
|---|---|---|
| C1 | Omit the full lower-bound Poisson correction | Rejected |
| C2 | Set the bound below the actual Poisson operator norm | Rejected |
| C3 | Drop Algorithm 1's `(m-1)` boundary multiplier | Stop changes from 93 to 7 |
| C4 | Remove `psi_t` from the boundary | 100/100 null paths falsely stop |
| C5 | Replace the composite GLR with a singleton SPRT objective | Objective mismatch detected |
| C6 | Correct-stationary MCMC and exact linear-MDP nulls | 0/100 MCMC rejections; 0/3 MDP controls reject |

The fixed command exits nonzero if a mutant is not detected or a required
valid-null control rejects.

[Open all raw evidence](../../evidence/)
