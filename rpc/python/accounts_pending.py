#!/usr/bin/env python3

import requests
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('account_ids', nargs='+',
                        help='account ID')
    return parser.parse_args()

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

args = parse_args()

params = {
  'action': 'accounts_pending',
  'accounts': args.account_ids,
  'count': 5,
  'include_only_confirmed': True,
}

print(params)
session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
