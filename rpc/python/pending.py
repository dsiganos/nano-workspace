#!/usr/bin/env python3

import requests
import json
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', type=int,
                        help='limit of number of blocks to return')
    parser.add_argument("account")
    return parser.parse_args()

def post(session, params):
    resp = session.post('http://[::1]:7076', json=params)
    return resp.json()

args = parse_args()

params = {
  "action": "pending",
  "account": args.account
}

if args.count != None:
    params["count"] = str(args.count)

session = requests.Session()
result = post(session, params)
print(json.dumps(result, indent=4))
