#!/usr/bin/env python3

# Script for RPC "block_create" command

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

    parser.add_argument('--work',
                        help='optional work value to use')

    parser.add_argument('wallet',
                        help='wallet ID holding account')

    parser.add_argument('account',
                        help='account that signs the block')

    parser.add_argument('previous',
                        help='previous block hash')

    parser.add_argument('representative',
                        help='representative to set in block')

    parser.add_argument('balance', type=int,
                        help='final balance for account after block creation')

    parser.add_argument('link',
                        help='link field in hex, send block hash or receive public key')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'block_create',
  'json_block': 'true',
  'type': 'state',
  'wallet': args.wallet,
  'account': args.account,
  'previous': args.previous,
  'representative': args.representative,
  'balance': str(args.balance),
  'link': args.link,
}

if args.work != None:
    params['work'] = args.work

print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url, timeout=360)
print(json.dumps(result, indent=4))
