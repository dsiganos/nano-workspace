#!/bin/env python3
import socket
import sys
import dns.resolver
import threading
import errno

tmo = 3

def get_all_dns_addresses(url):
    result = dns.resolver.resolve(url, 'A')
    return [ x.to_text() for x in result ]

def connect(to):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(tmo)
    try:
        sock.connect(to)
        print('%15s:%-5s connected' % to)
    except socket.timeout as e:
        print('%15s:%-5s FAILED, timeout after %s secs' % (*to,  tmo))
    except socket.error as e:
        print('%15s:%-5s FAILED, %s, %s' % (*to,  e.errno, e.strerror))

def parallel_connect(endpoints):
    threads = []
    for ip, port in endpoints:
        t = threading.Thread(target = lambda : connect((ip, port)))
        threads.append(t)
        t.start()
    return threads

print('Live nodes (peering.nano.org)')
live_endpoints = [ (x, 7075) for x in get_all_dns_addresses('peering.nano.org') ]
for t in parallel_connect(live_endpoints):
    t.join()

print('Beta nodes (peering-beta.nano.org)')
beta_endpoints = [ (x, 54000) for x in get_all_dns_addresses('peering-beta.nano.org') ]
for t in parallel_connect(beta_endpoints):
    t.join()

other_endpoints = [
    ('185.12.7.225',  7075),
    ('139.59.31.249', 7075),
    ('45.76.114.63',  7075),
]
print('Other nodes')
for t in parallel_connect(other_endpoints):
    t.join()
