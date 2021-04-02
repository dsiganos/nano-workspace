#!/bin/sh

if [ "$1" = "raw" ]; then
    curl -g -d '{ "action": "telemetry", "raw": "true" }' '[::1]:7076'
else
    curl -g -d '{ "action": "telemetry" }' '[::1]:7076'
fi
