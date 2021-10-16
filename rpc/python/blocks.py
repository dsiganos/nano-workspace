#!/usr/bin/env python3

import requests
import json
import argparse

import common

def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-b', '--beta', action='store_true', default=False,
                       help='use beta network')
    group.add_argument('-t', '--test', action='store_true', default=False,
                    help='use test network')

    parser.add_argument('--rpc',
                        help='RPC URL to contact')

    parser.add_argument("hash")

    return parser.parse_args()

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  "action": "blocks",
  "json_block": "true",
  "hashes": [args.hash]
}

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))
