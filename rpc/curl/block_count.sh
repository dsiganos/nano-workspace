#!/bin/sh

curl -g -d '{ "action": "block_count" }' '[::1]:7076'
