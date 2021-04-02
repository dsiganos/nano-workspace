#!/bin/sh

curl -g -d '{ "action": "stop" }' '[::1]:7076'
