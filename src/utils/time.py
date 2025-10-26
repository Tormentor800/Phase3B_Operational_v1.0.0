import pandas as pd

def utcnow_iso():
    return pd.Timestamp.utcnow().isoformat()

def to_local(ts, tz='UTC'):
    return pd.Timestamp(ts, tz='UTC').tz_convert(tz)
