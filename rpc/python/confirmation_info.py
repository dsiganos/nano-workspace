#!/usr/bin/env python3

# Create a random seed and a wallet using the seed created

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

    parser.add_argument('-r', '--root',
                        help='root to enquire about')

    parser.add_argument('-c', '--nocontents', action='store_true', default=False,
                       help='do not request contents')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

session = requests.Session()

if args.root != None:
    roots = [args.root]
else:
    # if a root was not given, then get roots via confirmation_active
    params = {
      'action': 'confirmation_active',
    }
    result = common.post(session, params, rpc_url)
    print(json.dumps(result, indent=4))
    roots = result['confirmations']

for root in roots:
    params = {
      'action': 'confirmation_info',
      'json_block': 'true',
      'root': root
    }
    if args.nocontents:
        params['contents'] = 'false'
    result = common.post(session, params, rpc_url)
    print(json.dumps(result, indent=4))
