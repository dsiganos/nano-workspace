#!/usr/bin/env python3

import json
import asyncio
import websockets
import time

params = {
  'action'  : 'subscribe',
  'topic' : 'started_election',
}

async def call_api(msg):
    async with websockets.connect('ws://127.0.0.1:17078') as websocket:
        await websocket.send(msg)
        async for message in websocket:
            print(message)

asyncio.get_event_loop().run_until_complete(call_api(json.dumps(params)))
