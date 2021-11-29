#!/usr/bin/env python3

# Script to send nano to itself. This will issue 2 transactions:
# a send to itself
# a receive of the send to itself

import requests
import json
import os
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

    parser.add_argument('account',
                        help='account to do the transactions on')

    parser.add_argument('amount', type=int,
                        help='amount in raw')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

id_str = os.urandom(32).hex()
print('id: %s' % id_str)

params = {
  'action': 'send',
  'wallet': args.wallet,
  'source': args.account,
  'destination': args.account,
  'amount': str(args.amount),
  'id': id_str,
}
print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url, timeout=360)
print(json.dumps(result, indent=4))

block = result['block']
assert len(block) == 64

params = {
  'action': 'receive',
  'account': args.account,
  'wallet': args.wallet,
  'account': args.account,
  'block': block,
}
print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url, timeout=360)
print(json.dumps(result, indent=4))
