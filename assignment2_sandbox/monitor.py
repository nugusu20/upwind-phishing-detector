import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


SANDBOX_DIR = Path("/sandbox_area")
LOGS_DIR = Path("/logs")
REPORTS_DIR = Path("/reports")
SAMPLE_PATH = Path("/samples/safe_sample.py")


def run_command(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    return result.stdout.strip()


def prepare_baseline_files() -> None:
    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
    (SANDBOX_DIR / "modified_by_sample.txt").write_text("Original content.\n")
    (SANDBOX_DIR / "deleted_by_sample.txt").write_text("This file should be deleted.\n")


def snapshot_files() -> dict[str, dict[str, float]]:
    snapshot = {}

    for path in SANDBOX_DIR.rglob("*"):
        if path.is_file():
            relative_path = str(path.relative_to(SANDBOX_DIR))
            stat = path.stat()
            snapshot[relative_path] = {
                "size": stat.st_size,
                "mtime": stat.st_mtime,
            }

    return snapshot


def compare_file_snapshots(before: dict, after: dict) -> dict[str, list[str]]:
    before_paths = set(before.keys())
    after_paths = set(after.keys())

    created = sorted(after_paths - before_paths)
    deleted = sorted(before_paths - after_paths)
    modified = sorted(
        path for path in before_paths & after_paths
        if before[path] != after[path]
    )

    return {
        "created": created,
        "deleted": deleted,
        "modified": modified,
    }


def write_report(file_changes: dict, process_snapshot: str, network_snapshot: str, sample_output: str) -> None:
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sample": str(SAMPLE_PATH),
        "file_changes": file_changes,
        "process_activity_snapshot": process_snapshot,
        "network_activity_snapshot": network_snapshot,
        "sample_output": sample_output,
    }

    (LOGS_DIR / "sandbox_log.json").write_text(json.dumps(report, indent=2))
    (REPORTS_DIR / "sandbox_report.txt").write_text(
        "Malware Analysis Sandbox Report\n"
        "================================\n\n"
        f"Sample executed: {SAMPLE_PATH}\n\n"
        "File changes:\n"
        f"- Created: {', '.join(file_changes['created']) or 'None'}\n"
        f"- Modified: {', '.join(file_changes['modified']) or 'None'}\n"
        f"- Deleted: {', '.join(file_changes['deleted']) or 'None'}\n\n"
        "Process activity snapshot:\n"
        f"{process_snapshot}\n\n"
        "Network activity snapshot:\n"
        f"{network_snapshot}\n"
    )


def main():
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    prepare_baseline_files()
    files_before = snapshot_files()

    sample_process = subprocess.Popen(
        ["python3", str(SAMPLE_PATH)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    time.sleep(0.5)

    process_snapshot = run_command(["ps", "-eo", "pid,ppid,comm,args"])
    network_snapshot = run_command(["ss", "-tunap"])

    sample_output, _ = sample_process.communicate()

    files_after = snapshot_files()
    file_changes = compare_file_snapshots(files_before, files_after)

    write_report(file_changes, process_snapshot, network_snapshot, sample_output)

    print("Sandbox execution completed.")
    print("Report written to /reports/sandbox_report.txt")
    print("Log written to /logs/sandbox_log.json")


if __name__ == "__main__":
    main()
