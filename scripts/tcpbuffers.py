#!/usr/bin/env python3
import argparse
import json
import logging
import re
import subprocess

def parse_address_and_port(address):
    "Parse an address string into an address and port"
    print('address: %s' % address)

    # Use regex to detect an IPv4 address
    match = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[.:](\d+)', address)
    if match:
        # Split the address and port
        address, port = match.groups()
    else:
        # Use regex to detect an IPv6 address
        match = re.match(r'([0-9a-fA-F:]+):(\d+)', address)
        if match:
        # Split the address and port
            address, port = match.groups()
    else:
        # Set the port to an empty string
        address, port = address, ''

    return address, port

def parse_netstat_line(line):
    "Parse a line of 'netstat' output into a dictionary"

    logging.debug(f'Parsing line: {line}')

    # Split the line into fields
    fields = line.split()

    logging.debug(f'Parsed fields: {fields}')

    # Create a dictionary for the connection
    connection = {
        'protocol': fields[0],
        'recv-q': int(fields[1]),
        'send-q': int(fields[2]),
        'local-address': fields[3],
        'foreign-address': fields[4],
        'state': fields[5]
    }
    print('connection:', connection)

    # Parse the local address and port
    address, port = parse_address_and_port(connection['local-address'])

    # Update the dictionary
    connection['local-address'] = address
    connection['local-port'] = port

    # Parse the foreign address and port
    address, port = parse_address_and_port(connection['foreign-address'])

    # Update the dictionary
    connection['foreign-address'] = address
    connection['foreign-port'] = port

    return connection

def parse_netstat_output(lines):
    "Parse the output of the 'netstat' command into a list of dictionaries"

    logging.debug(f'Parsing netstat output: {lines}')

    # Create a list to hold the connection dictionaries
    connections = []
    
    logging.debug(f'Created empty connections list')

    # Iterate over the lines
    for line in lines:
        # Check if the line is a TCP connection
        if 'tcp' in line:
            # Parse the line
            connection = parse_netstat_line(line)

            # Add the dictionary to the list
            connections.append(connection)

    return connections

def print_connections(connections):
    "Print a list of connection dictionaries in JSON format"
    print(json.dumps(connections, indent=4))

def list_large_tcp_buffers():
    "List all TCP socket buffers (receive or send) larger than 1 and print them in JSON format"

    logging.debug('Running netstat command')

    # Run the 'netstat' command to get socket information
    result = subprocess.run(['netstat', '-tn'], stdout=subprocess.PIPE)

    logging.debug(f'Netstat command output: {result.stdout.decode("utf-8")}')

    # Split the output into lines
    lines = result.stdout.decode('utf-8').split('\n')

    # Parse the output, filter out connections with 0 'recv-q' and 'send-q', and sort by 'send-q' in descending order
    connections = sorted([c for c in parse_netstat_output(lines) if c['recv-q'] > 0 or c['send-q'] > 0], key=lambda c: c['send-q'], reverse=True)

    # Print the sorted list of connections
    print_connections(connections)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose logging')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    list_large_tcp_buffers()
