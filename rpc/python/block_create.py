#!/usr/bin/env python3

# Script for RPC "block_create" command

import requests
import json
import argparse
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

    parser.add_argument('--process', action='store_true', default=False,
                        help='process the block after creating it')

    parser.add_argument('--work',
                        help='optional work value to use')

    parser.add_argument('-w', '--wallet',
                        help='wallet ID holding account')

    parser.add_argument('-a', '--account',
                        help='account that signs the block')

    parser.add_argument('-p', '--prvkey',
                        help='private key to sign the block (instead of wallet/account)')

    parser.add_argument('previous',
                        help='previous block hash')

    parser.add_argument('representative',
                        help='representative to set in block')

    parser.add_argument('balance', type=int,
                        help='final balance for account after block creation')

    parser.add_argument('link',
                        help='link field in hex, send block hash or receive public key')

    return parser.parse_args()


def process_block(session, rpc_url, blk, blkhash):
    print('Processing block with hash: %s' % blkhash)

    params = {
        "action": "process",
        "json_block": "true",
        "block": blk,
    }
    print(json.dumps(params, indent=4))

    result = common.post(session, params, rpc_url, timeout=360)
    print(json.dumps(result, indent=4))


args = parse_args()

if args.prvkey:
    if args.wallet or args.account:
        print('Private key given, wallet/account should not be set.')
        sys.exit(1)
else:
    if not args.wallet or not args.account:
        print('Wallet and account must be set, if private key is not used.')
        sys.exit(1)

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'block_create',
  'json_block': 'true',
  'type': 'state',
  'previous': args.previous,
  'representative': args.representative,
  'balance': str(args.balance),
  'link': args.link,
}

if args.wallet or args.account:
    params['wallet'] = args.wallet
    params['account'] = args.account
else:
    params['key'] = args.prvkey

if args.work != None:
    params['work'] = args.work

print(json.dumps(params, indent=4))

session = requests.Session()
result = common.post(session, params, rpc_url, timeout=360)
print(json.dumps(result, indent=4))

if args.process:
    print()
    process_block(session, rpc_url, result['block'], result['hash'])
