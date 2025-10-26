# Phase 3B Runbook (SOPs)

### CI failures
- Check PR logs on GitHub Actions.  
- Run pytest -q locally to reproduce.  

### Retrain job failures
- Inspect Actions â†’ Retrain log.  
- Typical causes: MLflow endpoint down, bad creds, missing validation file.  

### Promotion skipped
- Compare rtifacts/validation_ext/summary.json vs config/thresholds.yaml.  

### Monitoring alerts
- Open manifests/run_YYYYMMDD.json.  
- Check recent ingestion + metrics.  
- Roll back via previous model stage in MLflow Registry.  

### Secrets rotation
- Repo â†’ Settings â†’ Secrets and variables â†’ Actions:  
  - MLFLOW_TRACKING_URI  
  - MLFLOW_REGISTRY_URI  
  - SLACK_WEBHOOK_URL  
