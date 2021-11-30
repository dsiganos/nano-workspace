#!/usr/bin/env python3

import requests
import json
import argparse
import time
import datetime

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

    parser.add_argument('--csv', action='store_true', default=False,
                        help='sample every 10 seconds and write a CSV data')

    return parser.parse_args()


def get_block_count(session, rpc_url):
    params = {'action' : 'block_count'}
    result = common.post(session, params, rpc_url)
    count = int(result['count'])
    unchecked = int(result['unchecked'])
    cemented = int(result['cemented'])
    return result, count, unchecked, cemented


def produce_csv_values(session, rpc_url):
    print('count, timestamp (UTC), count, unchecked, cemented')
    i = 0
    lasttime = 0
    while True:
        if time.time() - lasttime > 10:
            timestamp = datetime.datetime.utcnow().strftime("%H:%M:%S")
            _, count, unchecked, cemented = get_block_count(session, rpc_url)
            print('%s, %s, %s, %s, %s' % (i, timestamp, count, unchecked, cemented))
            i += 1
            lasttime = time.time()
        time.sleep(0.1)


def single_block_count(session, rpc_url):
    result, count, unchecked, cemented = get_block_count(session, rpc_url)
    print(json.dumps(result, indent=4))
    print('count:      {:>15,}'.format(count))
    print('unchecked:  {:>15,}'.format(unchecked))
    print('cemented:   {:>15,}'.format(cemented))
    print('uncemented: {:>15,}'.format(count - cemented))
    print('total:      {:>15,}'.format(count + unchecked))


args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

session = requests.Session()

if args.csv:
    produce_csv_values(session, rpc_url)
else:
    single_block_count(session, rpc_url)
