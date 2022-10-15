#!/usr/bin/env python3

# Add an adhoc private key to a wallet

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

    parser.add_argument('wallet',
                        help='wallet ID')

    parser.add_argument('key',
                        help='adhoc private key')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'wallet_add',
  'wallet': args.wallet,
  'key': args.key,
}

session = requests.Session()
print(params)
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))
