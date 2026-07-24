# Candidate tests and release gate

The one inherited command on every experiment node is:

```bash
uv sync --frozen && uv run python repro/src/run_publication_gate.py
```

The accepted scientific run is `0a874377-72e3-48af-9134-d75c4d509b10`
at Git commit `69eb2f484b32ab603f856fd0fcdee1fd960fb4ba`.
It ran on local Apple M2 CPU in 18m12s and incurred no paid compute.

The claim-evidence gate passes C1–C6 and all legacy regressions. The repaired
release gate additionally requires:

- every required evidence file and exact verdict;
- the illustrated report and checked marimo notebook;
- the immutable judged file set as a subset of the candidate;
- a text-only upload allowlist and SHA-256 manifest;
- a byte-identical mirror of the faithful implementation inside the Space;
- an executable Space-root verifier that recomputes C1–C6;
- valid logbook JSON and reachable page paths;
- a repository and candidate secret scan.

The live judge gave the prior revision 5/12. The executable-evidence repair
is now published and awaiting a new verdict. No score increase is claimed
until that live verdict exists.
