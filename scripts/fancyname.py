#!/bin/env python3

import nanolib
import sys

while True:
    seed = nanolib.generate_seed()
    account_id = nanolib.generate_account_id(seed, 0)
    for word in sys.argv[1:]:
        if word in account_id:
            print()
            print('SEED  : %s' % seed)
            print('ACC ID: %s' % account_id)
