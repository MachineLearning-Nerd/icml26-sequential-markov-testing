# Limitations

The source omits the RBF bandwidth and random seeds; sigma=32 and all seeds are pinned here. MountainCar statistics are evaluated at six durable checkpoints rather than every reported 100 steps, although all 100,000 transitions and all 20 trials are generated. MCMC stopping times are interval-censored at 50 steps under the alternative and null checks use 250-step intervals.
