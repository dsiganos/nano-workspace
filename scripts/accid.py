#!/bin/env python3

import argparse
import nanolib


# known keys for testing
# privkey = 'B2ADC333DD83409956973E385573F05CFF04FFCF2DF9D2EBF4348C0D88769D46'
# pubkey  = '9413B858C932A559A78E95F74763B82A8C96BBBE49464FCDE91E8B11DD6C1ED5'
# acc_id  = 'nano_371mq3eekeo7d8mrx7hqaxjuicnektxuwkc8bz8yk9nd49gpr9podu3d6teo'


def parse_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--pubkey',
                       help='account ID to convert to public key')
    group.add_argument('-p', '--privkey',
                        help='private key to convert to public key')
    return parser.parse_args()


def main():
    args = parse_args()
    accid = nanolib.get_account_id(public_key=args.pubkey, private_key=args.privkey, prefix='nano_')
    print(accid)

main()
