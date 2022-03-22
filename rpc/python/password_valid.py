#!/usr/bin/env python3

# Is the password of a wallet set and the wallet unlocked

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

    parser.add_argument('password',
                        help='password')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'password_valid',
  'wallet': args.wallet,
  'password': args.password,
}
print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))
