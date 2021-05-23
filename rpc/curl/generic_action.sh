#!/bin/sh

curl -g -d "{ \"action\": \"$1\" }" '[::1]:7076'
