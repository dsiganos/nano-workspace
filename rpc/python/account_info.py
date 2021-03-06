#!/usr/bin/env python3

# Execute an RPc command of the form: {'action': action} 

import requests
import json
import argparse
import nanolib

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

    parser.add_argument('account',
                        help='account ID')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action'  : 'account_info',
  'account' : args.account,
  'include_confirmed' : 'true',
}

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))

raw_balance = int(result['balance'])
nano_balance = raw_balance / (10**30)
print('Unconfirmed Balance (Nano): %s' % '{:,}'.format(nano_balance))

confirmed_nano_balance = int(result['confirmed_balance']) / (10**30)
print('Confirmed   Balance (Nano): %s' % '{:,}'.format(confirmed_nano_balance))

pubkey = nanolib.get_account_public_key(account_id=args.account)
print('PUBKEY: %s' % pubkey.upper())
