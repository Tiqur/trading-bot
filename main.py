import asyncio
import websockets


async def client(address):
    async with websockets.connect(address) as websocket:
        while True:
            message = await websocket.recv()
            print(message)

asyncio.get_event_loop().run_until_complete(
    client('ws://localhost:5000'))
