#!/usr/bin/env python3

import asyncio
import websockets
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--host', dest='host', type=str, default='[::1]')
parser.add_argument('--port', dest='port', type=str, default='7078')
args = parser.parse_args()


def subscription(topic: str, ack: bool=False, options: dict=None):
    d = {"action": "subscribe", "topic": topic, "ack": ack}
    if options is not None:
        d["options"] = options
    return d

def update(topic: str, options: dict, ack: bool=False):
    return {"action": "update", "topic": topic, "ack": ack, "options": options}

def pretty(message):
    return json.dumps(message, indent=4)

async def main():
    async with websockets.connect(f"ws://{args.host}:{args.port}") as websocket:

        # Subscribe to both confirmation and votes
        # You can also add options here following instructions in
        # https://docs.nano.org/integration-guides/websockets/

        await websocket.send(json.dumps(subscription("confirmation", options={"include_election_info": "false", "include_block":"true"}, ack=True)))
        print(await websocket.recv()) # ack

        # V21.0+
        # await websocket.send(json.dumps(subscription("work", ack=True)))
        # print(await websocket.recv())  # ack

        while 1:
            rec = json.loads(await websocket.recv())
            topic = rec.get("topic", None)
            if topic:
                message = rec["message"]
                if topic == "confirmation":
                    print("Block confirmed:\n {}".format(pretty(message)))
                elif topic == "work":
                    print("Work:\n {}".format(pretty(message)))
                else:
                    print(topic, pretty(message))

try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    pass
except ConnectionRefusedError:
    print("Error connecting to websocket server. [node.websocket] enable=true must be set in ~/Nano/config-node.toml ; see host/port options with ./client.py --help")
