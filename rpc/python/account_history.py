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

    parser.add_argument('-c', '--count', type=int, default=-1,
                        help='limit of number of blocks to return')

    parser.add_argument('--raw', action='store_true', default=False,
                        help='request raw blocks')

    parser.add_argument('--reverse', action='store_true', default=False,
                        help='reverse the order of blocks')

    parser.add_argument('account')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'account_history',
  'account': args.account,
  'count': str(args.count),
  'raw': args.raw,
  'reverse': args.reverse,
}

print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))
