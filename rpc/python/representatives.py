#!/usr/bin/env python3

import requests
import json
import argparse

RPCURL = 'http://[::1]:7076'

def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

def post(session, params, timeout=5):
    resp = session.post(RPCURL, json=params, timeout=5)
    return resp.json()

args = parse_args()

params = {
  "action": "representatives",
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))

reps = result['representatives']
print(len(reps))

reps = { k:v for k,v in reps.items() if int(v) > 0 }

for rep in reps.items():
    print(rep)
print(len(reps))
