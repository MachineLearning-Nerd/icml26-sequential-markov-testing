# Method

MCMC uses the published target and exact good/bad 5×5 kernels with a convex stationary-distribution null. MDP uses Gymnasium MountainCar-v0, an 8×8 discretization, three actions, a uniform policy, ranks 3/5/7, 100,000 transitions, and 20 seeds. Each GLR is a constrained maximum-likelihood projection and the boundary is Algorithm 1's beta_t.
