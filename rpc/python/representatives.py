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

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  "action": "representatives",
}

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))

reps = result['representatives']
print(len(reps))

reps = { k:v for k,v in reps.items() if int(v) > 0 }

for rep in reps.items():
    print(rep)
print(len(reps))
