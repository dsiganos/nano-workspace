#!/usr/bin/env python3

# Create a random seed

import binascii
import secrets

def get_random_seed():
    return secrets.token_hex(32)

print('seed: %s' % get_random_seed())
