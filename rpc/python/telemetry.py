#!/usr/bin/env python3

import requests
import json
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--raw', action='store_true', default=False,
                        help='raw telemetry data')
    return parser.parse_args(sys.argv[1:])

args = parse_args()

if args.raw:
    params = {'action' : 'telemetry', 'raw' : 'true'}
else:
    params = {'action' : 'telemetry'}

session = requests.Session()
resp = session.post('http://[::1]:7076', json=params, timeout=5)
result = resp.json()

print(json.dumps(result, indent=4))
