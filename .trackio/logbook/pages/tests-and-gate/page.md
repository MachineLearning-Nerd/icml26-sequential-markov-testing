# Tests and gate


---
<!-- trackio-cell
{"type": "code", "id": "cell_0adb606d5bf8", "created_at": "2026-07-22T13:36:11+00:00", "title": "Clean gate command", "command": ["python3", "repro/src/run_publication_gate.py"], "exit_code": 0, "duration_s": 0.306}
-->
````bash
$ python3 repro/src/run_publication_gate.py
````

exit 0 · 0.3s


````python title=run_publication_gate.py
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable, "repro/src/verify_sequential_markov.py", "--output", "outputs/verification.json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
verification = json.loads((ROOT / "outputs/verification.json").read_text())
assert verification["verified_claims"] == 6 and verification["falsified_claims"] == 0
assert all(verification["negative_controls"].values())
gate = {"paper": "YEckWPoS09", "gate": "passed", "tests_passed": True, "publication_gate_passed": True,
        "verified_claims": 6, "scope": verification["scope"]}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))

````


````output
{
  "paper": "YEckWPoS09",
  "source_sha256": "2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8",
  "scope": "Source-pinned finite audit of lower-bound, Poisson-control, sequential-test, and application formulas; it does not independently prove the source's asymptotic results or alpha-correctness theorem.",
  "negative_controls": {
    "fixed_null_trace_not_rejected": true,
    "two_sided_not_one_sided_divergence": true,
    "equal_row_kernel_is_linear_compatible": true
  },
  "claims": {
    "C1": {
      "status": "verified",
      "anchor": "thm:lower_bound",
      "finite_cells": 4
    },
    "C2": {
      "status": "verified",
      "anchor": "lem:control_solution_poisson",
      "finite_cells": 4
    },
    "C3": {
      "status": "verified",
      "anchor": "alg:sequential_test",
      "stopping_time": 356
    },
    "C4": {
      "status": "verified",
      "anchor": "thm:optimality",
      "finite_cells": 3
    },
    "C5": {
      "status": "verified",
      "anchor": "thm:two_sided_test",
      "finite_cells": 3
    },
    "C6": {
      "status": "verified",
      "anchor": "MCMC and linear-MDP corollaries",
      "finite_cells": 2
    }
  },
  "verified_claims": 6,
  "falsified_claims": 0
}
test_six_source_pinned_claims (test_certificate.TestCertificate.test_six_source_pinned_claims) ... {
  "paper": "YEckWPoS09",
  "source_sha256": "2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8",
  "scope": "Source-pinned finite audit of lower-bound, Poisson-control, sequential-test, and application formulas; it does not independently prove the source's asymptotic results or alpha-correctness theorem.",
  "negative_controls": {
    "fixed_null_trace_not_rejected": true,
    "two_sided_not_one_sided_divergence": true,
    "equal_row_kernel_is_linear_compatible": true
  },
  "claims": {
    "C1": {
      "status": "verified",
      "anchor": "thm:lower_bound",
      "finite_cells": 4
    },
    "C2": {
      "status": "verified",
      "anchor": "lem:control_solution_poisson",
      "finite_cells": 4
    },
    "C3": {
      "status": "verified",
      "anchor": "alg:sequential_test",
      "stopping_time": 356
    },
    "C4": {
      "status": "verified",
      "anchor": "thm:optimality",
      "finite_cells": 3
    },
    "C5": {
      "status": "verified",
      "anchor": "thm:two_sided_test",
      "finite_cells": 3
    },
    "C6": {
      "status": "verified",
      "anchor": "MCMC and linear-MDP corollaries",
      "finite_cells": 2
    }
  },
  "verified_claims": 6,
  "falsified_claims": 0
}
ok

----------------------------------------------------------------------
Ran 1 test in 0.093s

OK
{
  "paper": "YEckWPoS09",
  "gate": "passed",
  "tests_passed": true,
  "publication_gate_passed": true,
  "verified_claims": 6,
  "scope": "Source-pinned finite audit of lower-bound, Poisson-control, sequential-test, and application formulas; it does not independently prove the source's asymptotic results or alpha-correctness theorem."
}

````
