#!/bin/sh

dir="`dirname "$0"`"
"$dir/../nano-build/nano_node" --wallet_list --data_path "$dir/../data"
