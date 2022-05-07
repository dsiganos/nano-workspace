#!/usr/bin/env python3

import requests
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', action='store_true', default=False,
                        help='Count delegators only')
    parser.add_argument("account")
    return parser.parse_args()

def post(session, params, timeout=60):
    resp = session.post('http://[::1]:7076', json=params, timeout=timeout)
    return resp.json()

args = parse_args()

action = 'delegators'
if args.count:
    action = 'delegators_count'

params = {
  "action": action,
  "account": args.account
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))

for delegator, weight in result['delegators'].items():
    weight_in_nano = int(weight) / (10**30)
    print('%s %s' % (delegator, '{:,}'.format(weight_in_nano)))
