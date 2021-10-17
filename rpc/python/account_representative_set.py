#!/usr/bin/env python3

import requests
import json
import argparse

import common

# example usage:
#./account_representative_set.py \
#   1CB0F1AD005BA3A9AAA111DFC9BC0FE120EF8BCC5C7920AD398935997BA8A5EC \
#   nano_1fofe3qxpisdgcymx9r3rptswp4mhny5mahnu3tdjgmti84f96694oj1beta \
#   nano_1fofe3qxpisdgcymx9r3rptswp4mhny5mahnu3tdjgmti84f96694oj1beta

RPCURL = 'http://[::1]:7076'

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
                        help='the wallet ID')

    parser.add_argument('account',
                        help='the account ID in nano_ format')

    parser.add_argument('representative',
                        help='the representative ID in nano_ format')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action'         : 'account_representative_set',
  'wallet'         : args.wallet,
  'account'        : args.account,
  'representative' : args.representative,
}

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))
