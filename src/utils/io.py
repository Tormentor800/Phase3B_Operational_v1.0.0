from pathlib import Path
import pandas as pd, json

def read_csv(path):
    return pd.read_csv(path)

def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2))

def read_json(path):
    return json.loads(Path(path).read_text())
