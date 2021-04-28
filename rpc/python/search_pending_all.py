#!/usr/bin/env python3

import requests
import json
import argparse

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

params = {
  'action': 'search_pending_all'
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
