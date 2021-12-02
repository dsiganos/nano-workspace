#!/usr/bin/env python3

# Create a pair of send/receive blocks representing a transfer

import requests
import json
import argparse
import nanolib

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

    parser.add_argument('-p', '--process', action='store_true', default=False,
                        help='Process the send and recv blocks (by default they are printed only)')

    parser.add_argument('--work1',
                        help='proof of work for send block')

    parser.add_argument('--work2',
                        help='proof of work for recv block')

    parser.add_argument('src_priv_key',
                        help='source account private key')

    parser.add_argument('tgt_priv_key',
                        help='target account private key')

    parser.add_argument('amount',
                        help='amount of raw to transfer')

    return parser.parse_args()


def privkey_to_accid(privkey):
    return nanolib.get_account_id(private_key=privkey, prefix='nano_')


def get_account_info(session, rpc_url, accid):
    params = {
      'action'  : 'account_info',
      'include_confirmed': 'true',
      'account' : accid,
    }
    result = common.post(session, params, rpc_url)
    #print(json.dumps(result, indent=4))
    return result


def get_account_representative(session, rpc_url, accid):
    params = {
      'action'  : 'account_representative',
      'account' : accid,
    }
    result = common.post(session, params, rpc_url)
    #print(json.dumps(result, indent=4))
    return result.get('representative', accid)


def block_create(prvkey, previous, representative, balance, link, work=None):
    params = {
        'action': 'block_create',
        'json_block': 'true',
        'type': 'state',
        'previous': previous,
        'representative': representative,
        'balance': str(balance),
        'link': link,
        'key': prvkey,
    }
    if work:
        params['work'] = work
    return params


def process_block(session, rpc_url, blk):
    params = {
        "action": "process",
        "json_block": "true",
        "block": blk,
    }
    print(json.dumps(params, indent=4))

    result = common.post(session, params, rpc_url, timeout=600)
    print(json.dumps(result, indent=4))


args = parse_args()

amount = int(args.amount)
session = requests.Session()
rpc_url = common.get_rpc_url(args)
print('RPC URL = %s' % rpc_url)

src_account = privkey_to_accid(args.src_priv_key)
tgt_account = privkey_to_accid(args.tgt_priv_key)
print('Transferring %s raw from %s to %s' % (amount, src_account, tgt_account))

src_acc_info = get_account_info(session, rpc_url, src_account)
src_balance_before = int(src_acc_info['confirmed_balance'])
assert src_balance_before >= amount
src_balance_after = src_balance_before - amount
print('Source Balance, before: %s, after: %s' % (src_balance_before, src_balance_after))

tgt_acc_info = get_account_info(session, rpc_url, tgt_account)
tgt_balance_before = int(tgt_acc_info.get('confirmed_balance', '0'))
tgt_balance_after = tgt_balance_before + amount
print('Target Balance, before: %s, after: %s' % (tgt_balance_before, tgt_balance_after))

src_acc_repr = get_account_representative(session, rpc_url, src_account)
tgt_acc_repr = get_account_representative(session, rpc_url, tgt_account)

send_block_params = block_create(args.src_priv_key, src_acc_info['confirmed_frontier'], \
                                 src_acc_repr, src_balance_after, \
                                 tgt_account, work=args.work1)
send_block_result = common.post(session, send_block_params, rpc_url, timeout=600)
print(json.dumps(send_block_result, indent=4))

send_block_hash = send_block_result['hash']

recv_block_previous = tgt_acc_info.get('confirmed_frontier', '0' * 64)
recv_block_params = block_create(args.tgt_priv_key, recv_block_previous, \
                          tgt_acc_repr, tgt_balance_after, \
                          send_block_hash, work=args.work2)
recv_block_result = common.post(session, recv_block_params, rpc_url, timeout=600)
print(json.dumps(recv_block_result, indent=4))

if args.process:
    process_block(session, rpc_url, send_block_result['block'])
    process_block(session, rpc_url, recv_block_result['block'])
