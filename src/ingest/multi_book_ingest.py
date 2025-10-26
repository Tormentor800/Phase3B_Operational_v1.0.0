from tenacity import retry, stop_after_attempt, wait_exponential_jitter
import pandas as pd, requests, time, logging
from .dq_checks import run_dq_checks

log = logging.getLogger('ingest')

@retry(stop=stop_after_attempt(5), wait=wait_exponential_jitter(1, 8))
def _pull(endpoint, params=None, timeout=10):
    r = requests.get(endpoint, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

def fetch_all_books(sources: dict[str,str]) -> pd.DataFrame:
    frames = []
    for name, url in sources.items():
        t0 = time.time()
        payload = _pull(url)
        df = pd.DataFrame(payload)
        df['source'] = name
        df['fetched_at'] = pd.Timestamp.utcnow()
        frames.append(df)
        log.info('fetched %s rows from %s in %.2fs', len(df), name, time.time()-t0)
    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    dq = run_dq_checks(out)
    if not dq['ok']:
        log.error('DQ failed: %s', dq['issues'])
        raise RuntimeError(f'DQ failure: {dq['issues']}")
    return out
