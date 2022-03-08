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

    group.add_argument('-i', '--notfound', action='store_true', default=False,
                       help='include not found')

    parser.add_argument('hashes', nargs='+')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  'action': 'blocks_info',
  'json_block': 'true',
  'pending': 'true',
  'source': 'true',
  'hashes': args.hashes
}
  
if args.notfound:
    params['include_not_found'] = 'true'

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))
