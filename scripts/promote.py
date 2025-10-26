# scripts/promote.py
import os
import mlflow
import pandas as pd

cfg = {
    "experiment_name": "Phase3/Models",
    "model_name": "phase3_model"
}

mlflow.set_tracking_uri("file:/tmp/mlruns")
mlflow.set_experiment(cfg["experiment_name"])
client = mlflow.tracking.MlflowClient()

def read_metrics(path):
    """Reads evaluation metrics from CSV file."""
    if not os.path.exists(path):
        print(f"[WARN] No metrics file found: {path}")
        return None
    try:
        df = pd.read_csv(path)
        return df.to_dict(orient="records")[0]
    except Exception as e:
        print(f"[ERROR] Failed to read metrics: {e}")
        return None

print("=== Starting Promotion Check ===")
new_metrics = read_metrics("artifacts/eval_metrics.csv")

if not new_metrics:
    print("[WARN] No new metrics found, skipping promotion.")
    raise SystemExit(0)

new_val = float(new_metrics.get("val_loss", "inf"))
run_id = new_metrics.get("run_id", "unknown")

try:
    versions = client.get_latest_versions(cfg["model_name"], stages=["Production"])
except Exception as e:
    print(f"[WARN] Could not fetch existing versions: {e}")
    versions = []

if not versions:
    print("[INFO] No existing production model found — promoting new model.")
    client.create_registered_model(cfg["model_name"])
    try:
        mv = client.create_model_version(
            name=cfg["model_name"],
            source=f"mlruns/{run_id}/artifacts/model",
            run_id=run_id,
        )
        client.transition_model_version_stage(cfg["model_name"], mv.version, stage="Production")
        print(f"[SUCCESS] Promoted initial model version {mv.version}")
    except Exception as e:
        print(f"[ERROR] Promotion failed: {e}")
    raise SystemExit(0)

prod = versions[0]
best_val = float(prod.tags.get("val_loss", "inf"))

if new_val < best_val:
    print(f"[SUCCESS] New model improved ({new_val} < {best_val}) → Promoting.")
    mv = client.create_model_version(
        name=cfg["model_name"],
        source=f"mlruns/{run_id}/artifacts/model",
        run_id=run_id,
    )
    client.transition_model_version_stage(cfg["model_name"], mv.version, stage="Production")
    client.set_model_version_tag(cfg["model_name"], mv.version, "val_loss", str(new_val))
else:
    print(f"[INFO] No improvement ({new_val} ≥ {best_val}) → Keeping current model.")
print("=== Promotion Step Complete ===")
