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

    parser.add_argument('-c', '--command', default='objects',
                        help='stat command to issue e.g. counters, objects')

    return parser.parse_args()


def get_stats(session, rpc_url, command):
    params = {'action': 'stats', 'type': command}
    return common.post(session, params, rpc_url)


def main():
    args = parse_args()

    rpc_url = common.get_rpc_url(args)
    print('RPC URL = %s' % rpc_url)

    session = requests.Session()
    result = get_stats(session, rpc_url, args.command)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
