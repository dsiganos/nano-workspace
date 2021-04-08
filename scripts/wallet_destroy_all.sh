#!/bin/sh

dir="`dirname "$0"`"

"$dir/wallet_list.sh" | grep 'Wallet ID: ' | cut -f 3 -d ' ' | xargs -n 1 "$dir/../rpc/python/wallet_destroy.py"
