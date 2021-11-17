#!/usr/bin/env python3

# Script for RPC "receive" command

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
                        help='receive wallet')

    parser.add_argument('account',
                        help='receive account')

    parser.add_argument('block',
                        help='hash of send block to receive')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'receive',
  'wallet': args.wallet,
  'account': args.account,
  'block': args.block,
}
print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url, timeout=360)
print(json.dumps(result, indent=4))
