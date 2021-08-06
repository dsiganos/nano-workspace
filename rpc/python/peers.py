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

params = {'action' : 'peers'}

if args.peerdetails:
    params['peer_details'] = 'true'

session = requests.Session()
resp = session.post('http://[::1]:7076', json=params, timeout=5)
result = resp.json()

print(json.dumps(result, indent=4))
