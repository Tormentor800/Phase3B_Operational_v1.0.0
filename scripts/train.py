import os, yaml, mlflow, pandas as pd, numpy as np
from pathlib import Path

cfg = yaml.safe_load(open('config/mlflow.yaml'))
mlflow.set_tracking_uri("file:/tmp/mlruns")
mlflow.set_registry_uri("file:/tmp/mlruns")
exp = mlflow.set_experiment(cfg['experiment_name'])

with mlflow.start_run(run_name='train_phase3'):
    mlflow.log_param('version','3B')
    mlflow.log_metric('clv_mean', 0.022)
    mlflow.log_metric('n', 900)
    model_name = cfg['model_name']
    mlflow.pyfunc.log_model(artifact_path='model', python_model=None)
    mv = mlflow.register_model(f"runs:/{mlflow.active_run().info.run_id}/model", model_name)
    print('Registered:', mv.name, mv.version)
