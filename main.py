import asyncio, websockets, json
prices = {}
alerts = []


async def client(address):
    async with websockets.connect(address, ping_interval=None) as websocket:
        while True:
            msg = json.loads(await websocket.recv())
            type = msg["type"]
            token = msg["token"]

            # Update prices
            if type == "price":
                price = msg["price"]

                # Update price
                if token in prices:
                    prices[token] = price
                else:
                    prices.update({token: price})
            
            # Add alert
            elif type == "alert":
                time = msg['time']
                interval = msg['interval']
                ema4 = msg['4ma']
                alerts.append({'token': token, 'time': time, 'interval': interval, '4ma': ema4})



asyncio.get_event_loop().run_until_complete(client('ws://localhost:5000'))
