#!/usr/bin/env python3

# Create a random seed and a wallet using the seed created

import requests
import json
import argparse
import os
import binascii

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', default=get_random_seed(),
                        help='seed to use for wallet')
    return parser.parse_args()

def get_random_seed():
    return binascii.b2a_hex(os.urandom(32)).decode('ascii')

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

args = parse_args()

params = {
  'action': 'wallet_create',
  'seed': args.seed,
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
print('seed: %s' % args.seed)
