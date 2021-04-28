#!/bin/sh

dir="`dirname "$0"`"
"$dir/../build/nano_node" --wallet_list --data_path "$dir/../data"
