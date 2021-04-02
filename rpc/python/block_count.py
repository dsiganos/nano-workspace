#!/usr/bin/env python3

import requests
import json

params = {'action' : 'block_count'}

session = requests.Session()
resp = session.post('http://[::1]:7076', json=params, timeout=5)
result = resp.json()

print(json.dumps(result, indent=4))
