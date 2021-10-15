import binascii
import os

def get_default_rpc_port(args):
    if args.beta:
        return 55000
    elif args.test:
        return 17076
    else:
        return 7076


def get_rpc_url(args):
    if args.rpc is not None:
        return args.rpc
    else:
        return 'http://[::1]:%s' % get_default_rpc_port(args)


def post(session, params, rpc_url, timeout=60):
    resp = session.post(rpc_url, json=params, timeout=timeout)
    return resp.json()


def get_random_seed():
    return binascii.b2a_hex(os.urandom(32)).decode('ascii')
