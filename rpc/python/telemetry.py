#!/usr/bin/env python3

import requests
import json
import sys
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

    parser.add_argument('-r', '--raw', action='store_true', default=False,
                        help='raw telemetry data')

    parser.add_argument('-m', '--max_block_count', action='store_true', default=False,
                        help='print the maximum block count seen in the network')

    return parser.parse_args(sys.argv[1:])

def average(lst):
    if len(lst) == 0: return 0
    return sum(lst) // len(lst)

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

if args.raw or args.max_block_count:
    params = {'action' : 'telemetry', 'raw' : 'true'}
else:
    params = {'action' : 'telemetry'}

session = requests.Session()
result = common.post(session, params, rpc_url)

if args.max_block_count:
    metrics = result['metrics']

    block_counts = [ int(x['block_count']) for x in metrics ]

    # sort metrics by block_count
    metrics.sort(key=lambda x: int(x['block_count']), reverse=True)

    # drop the smallest 20% of block counts (outliers), keep 80% largest
    limit = len(metrics) * 80 // 100
    metrics_filtered = metrics[:limit]

    # block counts of metrics filtered
    block_counts_filtered = [ int(x['block_count']) for x in metrics_filtered ]

    print('max:%s avg:%s min:%s' %
          (max(block_counts), average(block_counts_filtered), min(block_counts_filtered)))

elif args.raw:
    print(json.dumps(result, indent=4))

else:
    print(json.dumps(result, indent=4))
