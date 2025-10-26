import json, pandas as pd, numpy as np
from pathlib import Path
from src.utils.slack import post

def main():
    s = json.loads(Path('artifacts/validation_ext/summary.json').read_text())
    ok = (s['clv_pp_mean'] >= 0.010) and (s['n'] >= 300)
    man = {
      'status': 'OK' if ok else 'ALERT',
      'metrics': s,
      'timestamp': pd.Timestamp.utcnow().isoformat()
    }
    Path('manifests').mkdir(exist_ok=True)
    Path(f"manifests/run_{pd.Timestamp.utcnow():%Y%m%d}.json").write_text(json.dumps(man, indent=2))
    if not ok:
        post(f"Phase3B monitor: ALERT\nn={s['n']} clv_mean={s['clv_pp_mean']:.3%}")
    else:
        post(f"Phase3B monitor: OK\nn={s['n']} clv_mean={s['clv_pp_mean']:.3%}")

if __name__ == '__main__':
    main()
