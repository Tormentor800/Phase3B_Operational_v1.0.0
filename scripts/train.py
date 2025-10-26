import mlflow
import pandas as pd
import numpy as np
from pathlib import Path

# Force local file storage (no HTTP)
mlflow.set_tracking_uri("file:/tmp/mlruns")
mlflow.set_registry_uri("file:/tmp/mlruns")
mlflow.set_experiment("Phase3/Models")

class DummyModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        # simple placeholder prediction
        return np.ones(len(model_input)) * 0.5

with mlflow.start_run(run_name="train_phase3"):
    # log basic params + metrics
    mlflow.log_param("version", "3B")
    mlflow.log_metric("clv_mean", 0.022)
    mlflow.log_metric("n", 900)

    # log dummy model artifact
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=DummyModel(),
        conda_env=None
    )

    print("✅ Training complete. Model logged to /tmp/mlruns")
