import asyncio, websockets, json


class websocket_client:
    def __init__(self, address, prices, alerts):
        self.address = address
        self.prices = prices
        self.alerts = alerts
        self.start()

    def start(self):
        print("Connecting to server...")
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self.client(self.address))

    async def client(self, address):
        async with websockets.connect(address, ping_interval=None) as websocket:
            print("Connected!")
            while True:
                msg = json.loads(await websocket.recv())
                data_type = msg["type"]
                token = msg["token"]

                # Update prices
                if data_type == "price":
                    price = msg["price"]

                    # Update price
                    if token in self.prices:
                        self.prices[token] = price
                    else:
                        self.prices.update({token: price})
                
                # Add alert
                elif data_type == "alert":
                    time = msg['time']
                    interval = msg['interval']
                    ema4 = msg['4ma']
                    self.alerts.append({'token': token, 'time': time, 'interval': interval, '4ma': ema4})
