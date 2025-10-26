# Phase 3B â€“ Operationalization (CI/CD + MLflow + Monitoring)

### Overview
Self-contained operational bundle for Phase 3B of the SharpReady pipeline.

**Features**
- CI/CD (ruff + mypy + pytest + Docker release)  
- MLflow tracking and model registry integration  
- Scheduled retrain with auto promotion/demotion  
- Monitoring with Slack alerts and run manifests  
- Hardened multi-book ingest with retry/DQ/audit  
- Runbooks for maintenance and incident response  

**Quick Start**
`ash
pip install -r requirements.txt
python scripts/train.py
python scripts/evaluate.py
python scripts/promote.py
