# Command provenance

This is the complete command-level research provenance. Repeated polling is
collapsed with counts; it does not change code or evidence.

## Startup and source audit

```text
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
orx projects
orx runs d98973ef-8800-435c-aa86-6532ef555fc9
orx project view d98973ef-8800-435c-aa86-6532ef555fc9
git status --short
git rev-parse HEAD
git rev-parse origin/main
git branch -a
df -h .
sysctl -n machdep.cpu.brand_string
sysctl -n hw.logicalcpu
sysctl -n hw.memsize
env | sed 's/=.*//' | sort
```

The paper HTML and e-print were fetched with:

```text
curl -L --fail --silent --show-error -A 'OpenResearch-Reproduction-Audit/1.0 (contact: research-local)' https://ar5iv.labs.arxiv.org/html/2602.17587
curl -L --fail --silent --show-error -A 'OpenResearch-Reproduction-Audit/1.0 (contact: research-local)' https://export.arxiv.org/e-print/2602.17587
```

The live verdict dataset was downloaded at pinned revision
`2a3cad02b2d0111598a77e417e2737e99b956fbb`, then filtered with the exact
predicate `space_id == "DineshAI/YEckWPoS09"`. The judged Space was downloaded
with:

```text
hf download DineshAI/YEckWPoS09 --repo-type space --revision aa9d60e48d7ec637d6e5b8d37ba3bdaba95ef362
```

No token value or generated wrapper was printed.

## Experiment-tree mutations

```text
orx project edit d98973ef-8800-435c-aa86-6532ef555fc9 --run-command 'uv sync --frozen && uv run python repro/src/run_publication_gate.py'
orx create-experiment d98973ef-8800-435c-aa86-6532ef555fc9 --title 'Frozen judged baseline certificate' --run-command 'uv sync --frozen && uv run python repro/src/run_publication_gate.py'
orx create-experiment d98973ef-8800-435c-aa86-6532ef555fc9 --title 'Faithful core contracts and Algorithm 1' --parent e20d27e6-5bdc-4ef5-b1f9-1c7a3dd2fd77
orx create-experiment d98973ef-8800-435c-aa86-6532ef555fc9 --title 'Paper-scale MCMC and linear-MDP applications' --parent 52170fd8-3541-4117-a8ad-e5a5be88b78f
orx create-experiment d98973ef-8800-435c-aa86-6532ef555fc9 --title 'Corrected paper-scale application evidence' --parent 919a084d-a4c4-40c5-83ac-d31238dba8e4
orx create-experiment d98973ef-8800-435c-aa86-6532ef555fc9 --title 'Release candidate report and protected logbook' --parent ff3dc8e8-dd48-4a6c-8484-94e4501ef5c0
```

Each edited node used the standard Git sequence:

```text
git fetch origin
git checkout <orx branch>
git diff --check
git add <scoped paths>
git commit -m '<scoped message>'
git push origin <orx branch>
```

## Formal runs

Every run used exactly:

```text
orx exp run <experiment-id> --backend local
```

which executed the inherited command:

```text
uv sync --frozen && uv run python repro/src/run_publication_gate.py
```

Recorded runs:

| Run | Commit | Terminal state | Purpose |
|---|---|---|---|
| `47174994-aaaf-4168-8b54-66c588be9046` | `7600b72` | done | Frozen baseline |
| `f0e33ada-5fe5-4a2a-9148-8435f868ccc4` | `1c7e57a` | failed | Core JSON scalar diagnostic |
| `c45f6c0d-5c66-4bd9-90b0-e80662005cde` | `2c8e6b9` | failed | Core optimizer diagnostic |
| `60c046f6-cc57-44ce-b531-da3f287f7753` | `c1f05a9` | failed | Core checker diagnostic |
| `7aa28965-305c-48b5-9fd8-0c5ce5f4a401` | `892a204` | done | Accepted C1–C5 |
| `1788248d-6d5a-4c4c-91ab-ab7c2a051b05` | `606929b` | failed | MDP count-scaling diagnostic |
| `4f8d5a3d-69d3-448b-b00b-a9f1c5d439cd` | `fdcf090` | failed | Sparse-checkpoint diagnostic |
| `66b95921-9d51-4ada-9873-a6cccd412437` | `8a8687d` | failed | Inaccurate SCS checker rejected |
| `6433b609-5b60-4c29-bb8f-0162c8ae60f9` | `d75cf7d` | cancelled | Redundant diagnostic stopped |
| `8a31ac64-dfb5-4f60-bccd-0ea4081f8b25` | `6600699` | done | Solver-correct application diagnostic |
| `0a874377-72e3-48af-9134-d75c4d509b10` | `69eb2f4` | done | Accepted corrected C1–C6 |

Monitoring and evidence commands were:

```text
orx exp wait <experiment-id> --timeout 480
orx runs d98973ef-8800-435c-aa86-6532ef555fc9 --experiment <experiment-id>
orx logs <run-id> --bytes 1000000
orx exp cancel 919a084d-a4c4-40c5-83ac-d31238dba8e4
orx exp desc <experiment-id> --set '<evidence-backed description>'
orx exp status <experiment-id>
```

`orx exp wait ... --timeout 480` was repeated as needed while runs were active;
nonzero wait timeouts were reconciled with `orx runs` and never treated as run
failures.

## Lightweight validation and release packaging

```text
uv run python -m py_compile repro/src/run_applications.py
uv run python -m pytest -q repro/tests/test_markov_core.py
uv run python reports/claim-by-claim/generate_figures.py
uv run marimo check notebooks/sequential_markov_reproduction.py
uv run python repro/src/prepare_release.py
gh repo view MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing --json visibility,url,defaultBranchRef
```

Read-only diagnostics also used `rg`, `sed`, `find`, `shasum -a 256`, `du`,
`file`, `wc`, `ps`, and `git status/diff/log/ls-files/ls-remote`. Bulk `rsync`
and `cp` copied the immutable judged tree and accepted-run text artifacts into
the candidate without deleting source evidence.

## 5/12 verdict audit and executable-evidence repair

```text
orx projects --json
orx runs d98973ef-8800-435c-aa86-6532ef555fc9
orx create-experiment d98973ef-8800-435c-aa86-6532ef555fc9 --title 'Judge-visible executable claim evidence' --parent 74ed4503-75cd-433f-ab00-4659770a12c6
git checkout orx/judge-visible-executable-claim-evidence
uv run python repro/src/verify_judge_bundle.py
uv run python repro/src/prepare_release.py
uv run python -B .trackio/logbook/verify_candidate.py
```

The live verdict was selected only by
`space_id == "DineshAI/YEckWPoS09"`. The audited judged revision was
`66d5e67b5426622768e4d797656e409526f3a299`; its 99-file manifest contained
zero Python files. The repair makes the faithful implementation and independent
checker part of the exact text-only upload allowlist.

## Approved publication

```text
hf auth whoami
hf download DineshAI/YEckWPoS09 --type space --revision c9f4f905993eda348b395b80ea9aac9447f5a170 --local-dir <temporary-verification-directory> --quiet
hf download DineshAI/YEckWPoS09 --type space --revision a3b49a603d3777270e8e1cd11eb312f4e92efbe2 --local-dir <temporary-verification-directory> --quiet
git ls-remote origin refs/heads/main
```

The high-level `hf upload` command was rejected before committing because it
unnecessarily called the rate-limited repository-creation endpoint. The
existing Space remained unchanged. Publication then used
`HfApi.create_commit` directly against the existing repository with
`parent_commit` pinned:

- evidence commit `c9f4f905993eda348b395b80ea9aac9447f5a170` uploaded the exact
  91-file allowlist with zero deletions;
- metadata commit `a3b49a603d3777270e8e1cd11eb312f4e92efbe2` changed five existing
  pages to `PUBLISHED_AWAITING_JUDGE`;
- the final revision was independently downloaded, contained 109 files,
  retained both protected trees, and passed `verify_candidate.py` for C1–C6.

No token, credential value, or generated request wrapper was printed.
