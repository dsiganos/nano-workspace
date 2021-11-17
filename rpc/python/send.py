#!/usr/bin/env python3

# Script for RPC "send" command

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
                        help='wallet ID holding source account')

    parser.add_argument('source',
                        help='source account')

    parser.add_argument('destination',
                        help='destination account')

    parser.add_argument('amount', type=int,
                        help='amount in raw')

    parser.add_argument('id',
                        help='ID of transaction, must be unique everytime')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'send',
  'wallet': args.wallet,
  'source': args.source,
  'destination': args.destination,
  'amount': str(args.amount),
  'id': args.id,
}
print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url, timeout=360)
print(json.dumps(result, indent=4))
