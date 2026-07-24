# Faithful executable reproduction

These files are byte-for-byte mirrors of the implementation used by the fixed
OpenResearch command:

```text
uv sync --frozen && uv run python repro/src/run_publication_gate.py
```

The fast, judge-facing checker at [`../verify_candidate.py`](../verify_candidate.py)
recomputes the critical C1–C6 quantities from the raw evidence and exits nonzero
on any mismatch. From a downloaded Space revision:

```text
uv run --python 3.12 --with numpy==2.3.3 --with scipy==1.16.2 python verify_candidate.py
```

The complete application campaign can be rerun from the GitHub repository with
the fixed command above. Its pinned environment is recorded in
[`requirements.txt`](requirements.txt); the repository also contains the
authoritative `pyproject.toml` and `uv.lock`.

File roles:

- `markov_core.py`: empirical transition kernels, continuous composite GLR,
  row-wise KL statistic, adaptive boundary, pseudo-spectral gap, and Poisson
  solution.
- `run_core_campaign.py`: C1–C5 experiments, independent checks, and mutants.
- `run_applications.py`: the Appendix-G MCMC and MountainCar applications.
- `test_markov_core.py`: independent analytic unit checks.
- `source_manifest.json`: SHA-256 mapping to the authoritative repository files.
