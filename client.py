import asyncio, websockets, json


class websocket_client:
    def __init__(self, address, prices, alerts):
        self.address = address
        self.prices = prices
        self.alerts = alerts

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.client(self.address))

    async def client(self, address):
        async with websockets.connect(address, ping_interval=None) as websocket:
            while True:
                msg = json.loads(await websocket.recv())
                type = msg["type"]
                token = msg["token"]

                # Update prices
                if type == "price":
                    price = msg["price"]
                    print(price)

                    # Update price
                    if token in self.prices:
                        self.prices[token] = price
                    else:
                        self.prices.update({token: price})
                
                # Add alert
                elif type == "alert":
                    time = msg['time']
                    interval = msg['interval']
                    ema4 = msg['4ma']
                    self.alerts.append({'token': token, 'time': time, 'interval': interval, '4ma': ema4})
