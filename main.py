import threading
from client import *   
fees = {"spot": 0.01, "market": 0.05}

# Trading bot
class trading_bot():
    def __init__(self, fees, starting_amount):
        self.total = starting_amount
        self.fees = fees
        self.alerts = []
        self.trades = []
        self.prices = {}
        self.start()

    def market_buy(self):
        pass

    def exec_stop_loss(self, token, current_price, percent_below):
        pass
    
    def exec_trailing_stop_loss(self, token, current_price, percent_below):
        pass

    def market_sell(self):
        pass

    def start(self):
        # Initialize client
        thread = threading.Thread(target=websocket_client, args=('ws://localhost:5000', self.prices, self.alerts))
        thread.start()

        # Start bot
        while True:
            print(self.prices)
            
bot = trading_bot(fees, 1000)


