import os, yaml, json, mlflow
from pathlib import Path

thr = yaml.safe_load(open('config/thresholds.yaml'))['promotion']
summ = json.loads(Path('artifacts/validation_ext/summary.json').read_text())

meets = (
  (summ['n'] >= thr['n_min']) and
  (summ['clv_pp_mean'] >= thr['clv_mean_min']) and
  ((summ.get('p_value_clv') is None) or (summ['p_value_clv'] < thr['p_value_max']))
)

cfg = yaml.safe_load(open('config/mlflow.yaml'))
mlflow.set_tracking_uri(os.getenv('MLFLOW_TRACKING_URI', cfg['tracking_uri']))
mlflow.set_registry_uri(os.getenv('MLFLOW_REGISTRY_URI', cfg['registry_uri']))

client = mlflow.tracking.MlflowClient()
name = cfg['model_name']

if meets:
    latest = client.get_latest_versions(name, stages=['None','Staging','Production'])
    if latest:
        v = sorted(latest, key=lambda m: m.version)[-1].version
        client.transition_model_version_stage(name, v, stage='Production', archive_existing_versions=True)
        print(f'Promoted {name} v{v} -> Production')
else:
    print('Did not meet thresholds; no promotion.')
