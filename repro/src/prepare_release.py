from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
LOGBOOK = ROOT / ".trackio" / "logbook"
RELEASE = ROOT / "release"
REPORT = ROOT / "reports" / "claim-by-claim" / "report.md"
NOTEBOOK = ROOT / "notebooks" / "sequential_markov_reproduction.py"
FIXED_COMMAND = "uv sync --frozen && uv run python repro/src/run_publication_gate.py"
ACCEPTED_SHA = "69eb2f484b32ab603f856fd0fcdee1fd960fb4ba"

REQUIRED_CLAIM_FILES = {
    "claim_contract.json",
    "source_audit.md",
    "method.md",
    "independent_checker_output.json",
    "negative_control_output.json",
    "environment.json",
    "accepted_run.json",
    "verifier_output.json",
    "EVAL.md",
    "limitations_and_deviations.md",
}
ALLOWED_TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt"}
MUTABLE_OLD_PATHS = {"logbook.json", "pages/index.md"}
SECRET_PATTERNS = {
    "huggingface_token": re.compile(r"hf_[A-Za-z0-9]{20,}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(path: Path) -> list[str]:
    return [
        line.strip().removeprefix("./")
        for line in path.read_text().splitlines()
        if line.strip()
    ]


def parse_hashes(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text().splitlines():
        digest, relative = line.split(maxsplit=1)
        result[relative.removeprefix("./")] = digest
    return result


def validate_claim_artifacts() -> dict:
    verdicts = {}
    for index in range(1, 7):
        folder = ARTIFACTS / f"claim{index}"
        missing = sorted(name for name in REQUIRED_CLAIM_FILES if not (folder / name).is_file())
        assert not missing, f"claim{index} missing {missing}"
        contract = json.loads((folder / "claim_contract.json").read_text())
        verifier = json.loads((folder / "verifier_output.json").read_text())
        accepted = json.loads((folder / "accepted_run.json").read_text())
        assert contract["verdict"] == "VERIFIED"
        assert verifier["verdict"] == "VERIFIED"
        assert accepted["git_sha"] == ACCEPTED_SHA
        assert accepted["fixed_command"] == FIXED_COMMAND
        assert accepted["paid_cost_usd"] == 0
        verdicts[f"claim{index}"] = "VERIFIED"
    return verdicts


def validate_report() -> list[str]:
    report = REPORT.read_text()
    assert report.startswith("# Claim-by-claim reproduction")
    image_paths = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", report)
    assert len(image_paths) == 5
    assert len(set(image_paths)) == 5
    for relative in image_paths:
        image = REPORT.parent / relative
        assert image.is_file() and image.stat().st_size > 20_000
        assert image.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    subprocess.run(
        ["marimo", "check", str(NOTEBOOK.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
    )
    return image_paths


def validate_logbook() -> dict:
    data = json.loads((LOGBOOK / "logbook.json").read_text())
    assert data["space_id"] == "DineshAI/YEckWPoS09"
    children = data["root"]["children"]
    slugs = [child["slug"] for child in children]
    assert len(slugs) == len(set(slugs))
    for child in children:
        assert (LOGBOOK / child["file"]).is_file(), child["file"]
    return {"pages": len(children), "unique_slugs": True}


def validate_protected_subset() -> dict:
    old_paths = parse_manifest(RELEASE / "protected_judged_file_manifest.txt")
    old_hashes = parse_hashes(RELEASE / "protected_judged_sha256s.txt")
    candidate_paths = {
        path.relative_to(LOGBOOK).as_posix()
        for path in LOGBOOK.rglob("*")
        if path.is_file()
    }
    missing = sorted(set(old_paths) - candidate_paths)
    assert not missing
    changed = []
    preserved = []
    for relative in old_paths:
        if sha256(LOGBOOK / relative) == old_hashes[relative]:
            preserved.append(relative)
        else:
            changed.append(relative)
    assert set(changed) <= MUTABLE_OLD_PATHS
    result = {
        "judged_revision": "aa9d60e48d7ec637d6e5b8d37ba3bdaba95ef362",
        "old_file_count": len(old_paths),
        "candidate_file_count": len(candidate_paths),
        "old_paths_subset_of_candidate": True,
        "missing_old_paths": [],
        "byte_identical_old_paths": len(preserved),
        "navigation_files_changed_additively": sorted(changed),
    }
    (RELEASE / "old_new_subset_check.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def build_upload_allowlist() -> dict:
    old_paths = set(parse_manifest(RELEASE / "protected_judged_file_manifest.txt"))
    candidate_paths = sorted(
        path.relative_to(LOGBOOK).as_posix()
        for path in LOGBOOK.rglob("*")
        if path.is_file()
    )
    allowlist = [
        relative
        for relative in candidate_paths
        if relative not in old_paths or relative in MUTABLE_OLD_PATHS
    ]
    assert allowlist
    assert all(Path(relative).suffix in ALLOWED_TEXT_SUFFIXES for relative in allowlist)
    assert all((LOGBOOK / relative).read_bytes().decode("utf-8") is not None for relative in allowlist)
    (RELEASE / "hf_upload_allowlist.txt").write_text("\n".join(allowlist) + "\n")
    manifest_lines = [
        f"{sha256(LOGBOOK / relative)}  {relative}" for relative in allowlist
    ]
    (RELEASE / "hf_upload_sha256s.txt").write_text("\n".join(manifest_lines) + "\n")
    return {
        "files": len(allowlist),
        "text_only": True,
        "extensions": sorted({Path(relative).suffix for relative in allowlist}),
    }


def scan_secrets() -> dict:
    tracked = subprocess.run(
        ["git", "ls-files", "-co", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    candidates = {
        ROOT / relative
        for relative in tracked
        if (ROOT / relative).is_file()
        and (ROOT / relative).suffix.lower()
        in {".py", ".md", ".json", ".csv", ".txt", ".toml", ".lock", ".html", ".css", ".js"}
    }
    candidates.update(
        LOGBOOK / relative
        for relative in (RELEASE / "hf_upload_allowlist.txt").read_text().splitlines()
        if relative
    )
    findings = []
    for path in sorted(candidates):
        try:
            content = path.read_text()
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                findings.append(
                    {"path": path.relative_to(ROOT).as_posix(), "pattern": label}
                )
    assert not findings, f"secret-pattern findings in {[item['path'] for item in findings]}"
    result = {"files_scanned": len(candidates), "findings": 0}
    (RELEASE / "secret_scan.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main() -> None:
    verdicts = validate_claim_artifacts()
    report_images = validate_report()
    logbook = validate_logbook()
    subset = validate_protected_subset()
    upload = build_upload_allowlist()
    secrets = scan_secrets()
    summary = {
        "release_gate_passed": True,
        "publication_approved": False,
        "published": False,
        "fixed_command": FIXED_COMMAND,
        "claims": verdicts,
        "report_images": report_images,
        "logbook": logbook,
        "protected_subset": subset,
        "upload": upload,
        "secret_scan": secrets,
    }
    (RELEASE / "release_gate.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print("RELEASE_GATE_SUMMARY")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
