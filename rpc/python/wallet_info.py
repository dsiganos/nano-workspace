#!/usr/bin/env python3

import requests
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("wallet")
    return parser.parse_args()

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

args = parse_args()

params = {
  'action': 'wallet_info',
  'wallet': args.wallet,
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))

balance_in_nano = int(result['balance']) / 1e30
pending_in_nano = int(result['pending']) / 1e30
print('Balance in NANO: %s' % balance_in_nano)
print('Pending in NANO: %s' % pending_in_nano)
