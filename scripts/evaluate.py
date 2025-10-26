import json, pandas as pd, numpy as np, math, pathlib as P
from scipy import stats

sel = P.Path('artifacts/validation_ext/policy_selected_ext.csv')
df = pd.read_csv(sel)
clv = df['clv_pp'].dropna().to_numpy()
pnl = df['pnl'].dropna().to_numpy() if 'pnl' in df else np.array([])

def pval(arr):
    if len(arr)<2 or np.std(arr, ddof=1)==0:
        return None
    z = np.mean(arr)/(np.std(arr, ddof=1)/math.sqrt(len(arr)))
    return float(2*(1-stats.norm.cdf(abs(z))))

summary = {
  'n': int(len(df)),
  'clv_pp_mean': float(np.mean(clv)) if len(clv) else float('nan'),
  'clv_pp_median': float(np.median(clv)) if len(clv) else float('nan'),
  'p_value_clv': pval(clv),
  'p_value_pnl': pval(pnl) if len(pnl) else None
}
P.Path('artifacts/validation_ext/summary.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
