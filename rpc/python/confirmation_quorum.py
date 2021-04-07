#!/usr/bin/env python3

import requests
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--peerdetails', action='store_true', default=False,
                        help='Request peer details')
    return parser.parse_args()

args = parse_args()

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

params = {
  "action": "confirmation_quorum"
}

if args.peerdetails:
    params['peer_details'] = 'true'

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
