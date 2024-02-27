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

    parser.add_argument('-p', '--peerdetails', action='store_true', default=False,
                        help='Request peer details')

    return parser.parse_args()

args = parse_args()

rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

params = {
  "action": "confirmation_quorum"
}

if args.peerdetails:
    params['peer_details'] = 'true'

session = requests.Session()
result = common.post(session, params, rpc_url)
print(json.dumps(result, indent=4))

quorum_delta          = int(result['quorum_delta'])
online_weight_minimum = int(result['online_weight_minimum'])
online_stake_total    = int(result['online_stake_total'])
trended_stake_total   = int(result['trended_stake_total'])
peers_stake_total     = int(result['peers_stake_total'] )

print('online_weight_quorum_percent:', result['online_weight_quorum_percent'])
print('quorum_delta         :', "{:,} * (10**30)".format(quorum_delta // 10**30))
print('online_weight_minimum:', "{:,} * (10**30)".format(online_weight_minimum // 10**30))
print('online_stake_total   :', "{:,} * (10**30)".format(online_stake_total // 10**30))
print('trended_stake_total  :', "{:,} * (10**30)".format(trended_stake_total // 10**30))
print('peers_stake_total    :', "{:,} * (10**30)".format(peers_stake_total // 10**30))
print()
