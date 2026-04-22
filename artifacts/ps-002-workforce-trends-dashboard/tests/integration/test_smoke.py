import subprocess
import sys
import time
from pathlib import Path

import requests


DASHBOARD_PATH = (
    Path(__file__).resolve().parents[2]
    / "reports/dashboards/workforce_trends_dashboard.py"
)
URL = "http://localhost:8050"


def test_dashboard_serves_200():
    proc = subprocess.Popen(
        [sys.executable, str(DASHBOARD_PATH)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(Path(__file__).resolve().parents[4]),
    )
    try:
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                stdout, stderr = proc.communicate(timeout=1)
                raise AssertionError(
                    "Dashboard process exited before serving requests.\n"
                    f"stdout:\n{stdout}\n"
                    f"stderr:\n{stderr}"
                )
            try:
                resp = requests.get(URL, timeout=1)
                assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
                break
            except requests.RequestException:
                time.sleep(0.5)
        else:
            raise AssertionError(
                "Dashboard did not become ready on http://localhost:8050 within 30 seconds"
            )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
