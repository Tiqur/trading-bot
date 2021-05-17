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
        self._order(token, token_amount, 'limit', 'buy', limit)
        

    def limit_sell(self, token, token_amount, limit):
        self._order(token, token_amount, 'limit', 'sell', limit)


    def market_buy(self, token, token_amount):
        self._order(token, token_amount, 'market', 'buy')
        

    def market_sell(self, token, token_amount):
        self._order(token, token_amount, 'market', 'sell')
        

    # Private methods
    def _init(self):
        # Initialize client
        threading.Thread(target=websocket_client, args=('ws://localhost:5000', self.prices, self.alerts)).start()
        threading.Thread(target=self.exec_loop).start()


    def _exec_order(self, token, amount, type, order_type, order=None, limit_price=None):
        exec = True
        current_price = Decimal(self.prices[token])

        # If order is a limit buy / sell
        if limit_price:
            if type == 'buy' and current_price < limit_price or type == 'sell' and current_price > limit_price:
                exec = False

        if exec:
            print(f"Executed {order_type} {type} order for {current_price * amount if type == 'sell' else amount} {'stable' if type == 'sell' else token}( ${Decimal(current_price) * amount} )")
            new_stable_amt = Decimal(limit_price if limit_price else current_price) * amount
            new_stable_amt -= new_stable_amt * self.fees['spot' if limit_price else 'market']
            new_token_amt = amount

            if type == 'sell':
                new_stable_amt *= -1
                new_token_amt *= -1

            self.wallet[token] += new_token_amt
            self.wallet['stable'] -= new_stable_amt 

            # Pop 
            if order:
                self.orders.remove(order)


    def _order(self, token, token_amount, order_type, type, limit=None):
        # If token is not in wallet, initialize it
        if not token in self.wallet:
            self.wallet.update({token: 0})

        print(f"Placed {order_type} {type} order for {token_amount} {token}{f' at {limit}' if limit else ''}")
        if type == 'buy' or 'sell' and order_type == 'market' or 'limit':
            obj = {'type': type, 'order_type': order_type, 'token': token, 'amount': token_amount}

            # If market order, prioritize and call immediatly
            if not order_type == 'limit':
                self._exec_order(token, token_amount, type, order_type)
            else:
                obj.update({'limit': limit})

                # Append order to order queue
                self.orders.append(obj)

        else:
            raise Exception('Invalid limit / order type')
        

    def exec_loop(self):
        # Loop Executes orders and pops them off once filled
        while True:
            if self.orders:
                for order in self.orders:
                    # Execute order
                    limit = order['limit'] if 'limit' in order else None
                    self._exec_order(order['token'], order['amount'], order['type'], order['order_type'], order, limit)


                    

                        




