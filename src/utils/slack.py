import os, json, requests
WEBHOOK = os.getenv('SLACK_WEBHOOK_URL','')

def post(text:str, blocks=None):
    if not WEBHOOK:
        return
    payload = {'text': text}
    if blocks:
        payload['blocks'] = blocks
    r = requests.post(WEBHOOK, data=json.dumps(payload), headers={'Content-Type':'application/json'}, timeout=10)
    r.raise_for_status()
