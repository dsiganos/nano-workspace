#!/usr/bin/env python3

import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("seed")
args = parser.parse_args()

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

params = {
  "action": "deterministic_key",
  "seed": args.seed,
  "index": "0"
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
