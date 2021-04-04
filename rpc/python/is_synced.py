#!/usr/bin/env python3
#
# This script uses some heuristics to try and determine whether the local node is synced.
# The heuristics are:
#   Get the raw telemetry data from the local node.
#   If less than 100 metrics are received then fail due to insufficient data.
#   Remove the highest 10% and lowest 10% of block counts (outliers).
#   Calculate the average network block count after removing the outliers.
#   If the local block count is less than the average network block count then the local node is not synced.
#   Otherwise, it is deemed to be synced.

import requests
import json
import sys

def average(lst):
    if len(lst) == 0: return 0
    return sum(lst) // len(lst)

def post(session, params, timeout=5):
    resp = session.post('http://[::1]:7076', json=params, timeout=5)
    return resp.json()

session = requests.Session()

# obtain raw telemetry data
metrics = post(session, {'action' : 'telemetry', 'raw' : 'true'})['metrics']

# we want to see at least 100 results
if len(metrics) < 100:
    print('ERROR: not enough telemetry data, only %d metrics received' % len(metrics))
    sys.exit(1)

# sort metrics by block_count
metrics.sort(key=lambda x: int(x['block_count']), reverse=True)

# drop the first 10% and last 10% (outliers)
a = len(metrics) * 10 // 100
b = len(metrics) * 90 // 100
metrics_filtered = metrics[a:b]

# extract the block counts only from the filtered metrics
block_counts_filtered = [ int(x['block_count']) for x in metrics_filtered ]

# calculate the average of the filtered block counts
average_block_count = average(block_counts_filtered)

# now get the local node block count and compare it to average network block count
local_block_count = int(post(session, {'action' : 'block_count'})['count'])
diff = local_block_count - average_block_count

print('Local block count: %s, Average network block count: %s, Diff: %s' %
      (local_block_count, average_block_count, diff))

if diff < 0:
    print('ERROR: the local node is not synced sufficiently')
    sys.exit(1)

print('SUCCESS: local node is synced!')
sys.exit(0)
