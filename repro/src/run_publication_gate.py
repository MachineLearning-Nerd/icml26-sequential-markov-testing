import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
subprocess.run([sys.executable, "repro/src/verify_sequential_markov.py", "--output", "outputs/verification.json"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_core_campaign.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/run_applications.py"], cwd=ROOT, check=True)
subprocess.run(
    [
        sys.executable,
        "repro/src/verify_judge_bundle.py",
        "--output",
        ".openresearch/artifacts/judge_visible_verifier.json",
    ],
    cwd=ROOT,
    check=True,
)
subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "repro/tests", "-v"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "reports/claim-by-claim/generate_figures.py"], cwd=ROOT, check=True)
subprocess.run([sys.executable, "repro/src/prepare_release.py"], cwd=ROOT, check=True)
verification = json.loads((ROOT / "outputs/verification.json").read_text())
core = json.loads((ROOT / ".openresearch/artifacts/core_summary.json").read_text())
application = json.loads((ROOT / ".openresearch/artifacts/application_summary.json").read_text())
judge_visible = json.loads((ROOT / ".openresearch/artifacts/judge_visible_verifier.json").read_text())
release = json.loads((ROOT / "release/release_gate.json").read_text())
assert verification["verified_claims"] == 6 and verification["falsified_claims"] == 0
assert all(verification["negative_controls"].values())
assert set(core["results"].values()) == {"VERIFIED"}
assert application["verdict"] == "VERIFIED"
assert judge_visible["verdict"] == "VERIFIED"
assert set(judge_visible["claims"]) == {f"claim{index}" for index in range(1, 7)}
assert release["release_gate_passed"]
gate = {
    "paper": "YEckWPoS09",
    "gate": "release-candidate-ready",
    "tests_passed": True,
    "publication_gate_passed": False,
    "release_gate_passed": True,
    "publication_approved": False,
    "published": False,
    "legacy_regression_passed": True,
    "core_claims": core["results"],
    "application_claim": application["verdict"],
    "judge_visible_claims": {
        name: claim["verdict"] for name, claim in judge_visible["claims"].items()
    },
    "remaining_claims": [],
    "scope": "C1-C6 evidence and all release checks passed. Publication remains closed until explicit user approval.",
}
(ROOT / "outputs/publication_gate.json").write_text(json.dumps(gate, indent=2) + "\n")
print(json.dumps(gate, indent=2))
