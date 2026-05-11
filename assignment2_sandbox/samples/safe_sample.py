import socket
import subprocess
import time
from pathlib import Path


SANDBOX_DIR = Path("/sandbox_area")


def simulate_file_activity():
    created_file = SANDBOX_DIR / "created_by_sample.txt"
    modified_file = SANDBOX_DIR / "modified_by_sample.txt"
    deleted_file = SANDBOX_DIR / "deleted_by_sample.txt"

    created_file.write_text("This file was created by the safe sample.\n")
    modified_file.write_text("Modified content by the safe sample.\n")

    if deleted_file.exists():
        deleted_file.unlink()


def simulate_process_activity():
    return subprocess.Popen(["sh", "-c", "sleep 2"])


def simulate_network_activity():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 4444))
    server_socket.listen(1)
    time.sleep(2)
    server_socket.close()


def main():
    simulate_file_activity()
    child_process = simulate_process_activity()
    simulate_network_activity()
    child_process.wait()


if __name__ == "__main__":
    main()
