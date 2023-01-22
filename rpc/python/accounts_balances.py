#!/usr/bin/env python3

import requests
import json
import argparse
import nanolib
import sys

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

    parser.add_argument('accounts', nargs='+',
                        help='account ID')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action'  : 'accounts_balances',
  'accounts' : args.accounts,
}

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))

if result.get('error') is not None:
    print(result.get('error'))
    sys.exit(1)

balances = result['balances']
for acc in balances:
    print(acc)
    print('    %s' % balances[acc])
