#!/bin/env python3
import socket
import sys
import dns.resolver

def get_all_dns_addresses(url):
    result = dns.resolver.resolve(url, 'A')
    return [ x.to_text() for x in result ]

def connect(to):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    print('%15s:%-5s ' % to, end='')
    try:
        sock.connect(to)
        print('connected')
    except:
        print('NOT connected')

print('Live nodes')
for node in get_all_dns_addresses('peering.nano.org'):
    connect((node, 7075))

print('Beta nodes')
for node in get_all_dns_addresses('peering-beta.nano.org'):
    connect((node, 54000))
