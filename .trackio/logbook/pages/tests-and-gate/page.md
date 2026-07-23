# Candidate tests and release gate

The one inherited command on every experiment node is:

```bash
uv sync --frozen && uv run python repro/src/run_publication_gate.py
```

The accepted scientific run is `0a874377-72e3-48af-9134-d75c4d509b10`
at Git commit `69eb2f484b32ab603f856fd0fcdee1fd960fb4ba`.
It ran on local Apple M2 CPU in 18m12s and incurred no paid compute.

The cumulative release-candidate run passed C1–C6, every legacy regression,
and the following publication checks:

- every required evidence file and exact verdict;
- the illustrated report and checked marimo notebook;
- the immutable judged file set as a subset of the candidate;
- a text-only upload allowlist and SHA-256 manifest;
- valid logbook JSON and reachable page paths;
- a repository and candidate secret scan.

The additive text-only Space release was explicitly approved and published on
2026-07-23. The paper is awaiting live-judge evaluation; the public score
remains 4/12 until a new verdict is issued.
