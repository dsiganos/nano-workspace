#!/usr/bin/env python3

import requests
import json

params = {'action' : 'block_count'}

session = requests.Session()
resp = session.post('http://[::1]:7076', json=params, timeout=5)
result = resp.json()

print(json.dumps(result, indent=4))

count = int(result['count'])
unchecked = int(result['unchecked'])
cemented = int(result['cemented'])
print('count:      {:>15,}'.format(count))
print('unchecked:  {:>15,}'.format(unchecked))
print('cemented:   {:>15,}'.format(cemented))
print('uncemented: {:>15,}'.format(count - cemented))
print('total:      {:>15,}'.format(count + unchecked))
