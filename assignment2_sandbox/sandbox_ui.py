import subprocess
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
REPORT_PATH = BASE_DIR / "reports" / "sandbox_report.txt"
LOG_PATH = BASE_DIR / "logs" / "sandbox_log.json"
CONTAINER_NAME = "upwind-malware-sandbox-run"
IMAGE_NAME = "upwind-malware-sandbox:1.0"


def run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text()
    return "No report generated yet."


def is_container_running() -> bool:
    result = run_command([
        "docker",
        "ps",
        "--filter",
        f"name={CONTAINER_NAME}",
        "--format",
        "{{.Names}}",
    ])
    return CONTAINER_NAME in result.stdout


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "sandbox.html",
        report=read_file(REPORT_PATH),
        log=read_file(LOG_PATH),
        running=is_container_running(),
    )


@app.route("/start", methods=["POST"])
def start_sandbox():
    if not is_container_running():
        run_command([
            "docker",
            "run",
            "--rm",
            "--name",
            CONTAINER_NAME,
            "--network",
            "none",
            "-v",
            f"{BASE_DIR / 'logs'}:/logs",
            "-v",
            f"{BASE_DIR / 'reports'}:/reports",
            IMAGE_NAME,
        ])

    return redirect(url_for("index"))


@app.route("/stop", methods=["POST"])
def stop_sandbox():
    if is_container_running():
        run_command(["docker", "stop", CONTAINER_NAME])

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
