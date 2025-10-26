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
    if not os.path.exists(path):
        print(f"No metrics file found: {path}")
        return None
    df = pd.read_csv(path)
    return df.to_dict(orient="records")[0]

new_metrics = read_metrics("artifacts/eval_metrics.csv")
if not new_metrics:
    raise SystemExit("No new metrics available")

try:
    versions = client.get_latest_versions(cfg["model_name"], stages=["Production"])
    if not versions:
        print("No existing Production model — promoting new one.")
        promote = True
        best_val = None
    else:
        prod = versions[0]
        best_val = float(prod.tags.get("val_loss", "inf"))
        promote = float(new_metrics["val_loss"]) < best_val
except Exception:
    print("No previous model or unable to fetch — defaulting to promote new one.")
    promote = True

if promote:
    print(f"Promoting new model (val_loss={new_metrics['val_loss']}, best={best_val})")
    run_id = new_metrics.get("run_id", None)
    client.create_model_version(cfg["model_name"], source=f"mlruns/{run_id}/artifacts/model", run_id=run_id)
    client.transition_model_version_stage(cfg["model_name"], 1, stage="Production")
else:
    print(f"No improvement (val_loss={new_metrics['val_loss']} ≥ {best_val}), keeping current model.")
