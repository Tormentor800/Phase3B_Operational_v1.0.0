# scripts/monitor.py
import os
import json
import mlflow
from datetime import datetime, timezone

# MLflow configuration
MLRUNS_PATH = "/tmp/mlruns"
ARTIFACTS_DIR = "artifacts"
MANIFEST_PATH = os.path.join(ARTIFACTS_DIR, "run_manifest.json")

# Make sure artifacts directory exists
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

def get_latest_run():
    """Return metadata for the most recent MLflow run."""
    if not os.path.exists(MLRUNS_PATH):
        return None

    latest_run = None
    latest_time = 0

    for root, _, files in os.walk(MLRUNS_PATH):
        if "meta.yaml" in files:
            path = os.path.join(root, "meta.yaml")
            mtime = os.path.getmtime(path)
            if mtime > latest_time:
                latest_time = mtime
                latest_run = path

    if not latest_run:
        return None

    return {
        "path": latest_run,
        "last_modified": datetime.fromtimestamp(latest_time, tz=timezone.utc).isoformat()
    }

def build_manifest():
    """Create a monitoring manifest JSON summarizing pipeline status."""
    latest = get_latest_run()
    manifest = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": "OK" if latest else "NO_RUNS_FOUND",
        "latest_run": latest,
    }

    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[INFO] Monitoring manifest written to {MANIFEST_PATH}")
    print(json.dumps(manifest, indent=2))
    return manifest

if __name__ == "__main__":
    print("=== Starting Pipeline Health Check ===")
    manifest = build_manifest()
    print("=== Health Check Complete ===")
