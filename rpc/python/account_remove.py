#!/usr/bin/env python3

# Create a random seed and a wallet using the seed created

import requests
import json
import argparse
import os
import binascii

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('wallet',
                        help='wallet ID')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--account',
                       help='account ID')
    group.add_argument('--all', action='store_true', default=False,
                        help='remove all accounts in wallet')
    return parser.parse_args()

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

def get_account_list(session, wallet):
    params = {'action': 'account_list', 'wallet': wallet}
    session = requests.Session()
    return post(session, params)['accounts']

def account_remove(session, wallet, account):
    print('Removing account %s from wallet %s' % (account, wallet))
    params = {
      'action':  'account_remove',
      'wallet':  wallet,
      'account': account,
    }
    result = post(session, params)
    print(json.dumps(result, indent=4))

args = parse_args()
session = requests.Session()

if args.all:
    acc_list = get_account_list(session, args.wallet)
    for a in acc_list:
        account_remove(session, args.wallet, a)
else:
    account_remove(session, args.wallet, args.account)
