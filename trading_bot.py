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
        self._init()
    
    # Public methods
    def limit_buy(self, token, token_amount, limit):
        self._order(token, 'limit', 'buy', token_amount, limit)
        
    def limit_sell(self, token, token_amount, limit):
        self._order(token, 'limit', 'sell', token_amount, limit)

    def market_buy(self, token, token_amount):
        self._order(token, 'market', 'buy', token_amount)
        
    def market_sell(self, token, token_amount):
        self._order(token, 'market', 'sell', token_amount)
        
    # Private methods
    def _init(self):
        # Initialize client
        threading.Thread(target=websocket_client, args=('ws://localhost:5000', self.prices, self.alerts)).start()
        threading.Thread(target=self.exec_loop).start()

    def _exec_order(self, token, amount, type, limit_price=None):
        exec = True
        current_price = self.prices[token]

        # If order is a limit buy / sell
        if limit_price:
            if type == 'buy' and current_price < limit_price or type == 'sell' and current_price > limit_price:
                exec = False

        if exec:
            print(f"Executed {order} {type} order for {current_price * amount if type == 'sell' else amount} {'stable' if type == 'sell' else token}( ${current_price * amount} )")
            mul_stable = limit_price if limit_price else current_price
            new_stable_amt = mul_stable * token
            new_token_amt = amount

            if type == 'sell':
                new_stable_amt *= -1
                new_token_amt *= -1


            self.wallet[token] += new_token_amt
            self.wallet['stable'] -= new_stable_amt - new_stable_amt * self.fees['spot' if limit_price else 'market']

    def _order(self, token, token_amount, order, type, limit=None):
        print(f"Placed {order} {type} order for {amount} {token}{f'at {limit}' if limit else ''}")
        if type == 'buy' or 'sell' and order == 'market' or 'limit':
            obj = {'type': f"{order}_{type}", 'token': token, 'amount': token_amount}
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
                    limit = order['limit'] if 'limit' in order else None
                    self._exec_order(order, token, amount, limit)


                    

                        




