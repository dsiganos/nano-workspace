#!/usr/bin/env python3

import requests
import json
import argparse

# example usage:
#./account_representative_set.py \
#   1CB0F1AD005BA3A9AAA111DFC9BC0FE120EF8BCC5C7920AD398935997BA8A5EC \
#   nano_1fofe3qxpisdgcymx9r3rptswp4mhny5mahnu3tdjgmti84f96694oj1beta \
#   nano_1fofe3qxpisdgcymx9r3rptswp4mhny5mahnu3tdjgmti84f96694oj1beta

RPCURL = 'http://[::1]:7076'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('wallet',
                        help='the wallet ID')
    parser.add_argument('account',
                        help='the account ID')
    parser.add_argument('representative',
                        help='the representative ID')
    return parser.parse_args()

def post(session, params, timeout=60):
    resp = session.post(RPCURL, json=params, timeout=timeout)
    return resp.json()

args = parse_args()

params = {
  'action'         : 'account_representative_set',
  'wallet'         : args.wallet,
  'account'        : args.account,
  'representative' : args.representative,
}

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
