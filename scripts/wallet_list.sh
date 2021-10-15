#!/bin/sh

if [ "$1" != "" -a "$1" != "beta" -a "$1" != "test" ]; then
    echo beta or test argument expected
    exit 1
fi

network=${1:-live}
data_prefix=${1}


dir="`dirname "$0"`"
"$dir/../build/nano_node" --wallet_list --data_path "$dir/../${data_prefix}data" --network $network
