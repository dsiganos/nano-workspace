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

params = {
  "action": "representatives",
}

session = requests.Session()
result = common.post(session, params, rpc_url)

reps = result['representatives']

reps = { k:int(v) for k,v in reps.items() if int(v) > 0 }

reps_list_sorted = sorted(reps.items(), key = lambda x:x[1], reverse=True)

supply = 133248297 * 10 ** 30

for k, v in reps_list_sorted:
    perc = v * 100 / supply
    print(k, '{: >6.3f}'.format(perc), v)
print(len(reps))
