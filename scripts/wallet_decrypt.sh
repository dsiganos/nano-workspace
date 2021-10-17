#!/bin/sh

wallet=$1
if [ -z "$wallet" ]; then
    echo wallet expected as first argument
    exit 1
fi

if [ "$2" != "" -a "$2" != "beta" -a "$2" != "test" ]; then
    echo beta or test argument expected
    exit 1
fi

network=${2:-live}
data_prefix=${2}


dir="`dirname "$0"`"
"$dir/../build/nano_node" --wallet_decrypt_unsafe --wallet=$wallet \
    --data_path "$dir/../${data_prefix}data" --network $network
