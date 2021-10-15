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

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {'action' : 'block_count'}

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))

count = int(result['count'])
unchecked = int(result['unchecked'])
cemented = int(result['cemented'])
print('count:      {:>15,}'.format(count))
print('unchecked:  {:>15,}'.format(unchecked))
print('cemented:   {:>15,}'.format(cemented))
print('uncemented: {:>15,}'.format(count - cemented))
print('total:      {:>15,}'.format(count + unchecked))
