import numpy as np

def run_dq_checks(df):
    issues = []
    if df.empty:
        issues.append('empty_frame')
    for col in ['exec_odds','clv_pp','market','ttc_minutes']:
        if col not in df.columns:
            issues.append(f'missing:{col}')
    if 'exec_odds' in df and np.nan_to_num(df['exec_odds']).max() <= 0:
        issues.append('bad_odds')
    return {'ok': len(issues)==0, 'issues': issues}
