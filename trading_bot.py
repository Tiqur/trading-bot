import threading, time
from client import *   
from decimal import *

# Trading bot
class TradingBot():
    def __init__(self, fees, starting_amount):
        self.fees = fees
        self.alerts = []
        self.orders = []
        self.trades = []
        self.prices = {}
        self.wallet = {'stable': Decimal(starting_amount)}
        self.init()
    
    def init(self):
        # Initialize client
        threading.Thread(target=websocket_client, args=('ws://localhost:5000', self.prices, self.alerts)).start()
        threading.Thread(target=self.exec_loop).start()

    def order(self, token, token_amount, order, type, limit=None):
        if type == 'buy' or 'sell' and order == 'market' or 'limit':
            obj = {'type': f"{order}_{type}", token: token, amount: amount}
            if order == 'limit':
                obj.update({'limit': limit})
        else:
            raise Exception('Invalid limit / order type')
        

    def exec_loop(self):
        # Loop Executes orders and pops them off once filled
        while True:
            if self.orders:
                for order in self.orders:
                    type = order['type']
                    token = order['token']
                    amount = order['amount']
                    

                        




