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
    def limit_buy(self, token, stable_amount, limit):
        self._order(token, stable_amount, 'limit', 'buy', limit)
        

    def limit_sell(self, token, stable_amount, limit):
        self._order(token, stable_amount, 'limit', 'sell', limit)


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
        current_price = Decimal(self.prices[token])
        
        # If order is a limit buy / sell
        if (limit_price and type == 'buy' and current_price > limit_price) or (limit_price and type == 'sell' and current_price < limit_price) or not limit_price:
            current_price = Decimal(limit_price if limit_price else current_price)
            fees = self.fees['spot' if limit_price else 'market']


            # If buy, amount is the amount of stable coins to spend
            if type == 'buy':
                amount_with_fees = amount - amount * fees
                self.wallet[token] += amount_with_fees / current_price
                self.wallet['stable'] -= amount
                print(f"Executed {order_type} {type} order for {round(amount_with_fees / current_price, 4)} {token} at {round(current_price, 4)} ( ${round(amount, 2)} )")

            # If sell, amount is the amount of tokens to sell
            else: 
                new_stable = amount * current_price
                new_stable_with_fees = new_stable - new_stable * fees
                self.wallet[token] -= amount
                self.wallet['stable'] +=  new_stable_with_fees
                print(f"Executed {order_type} {type} order for {round(new_stable_with_fees, 4)} stable at {round(current_price, 4)} ( ${round(new_stable_with_fees, 2)} )")

            # Pop 
            if order:
                self.orders.remove(order)

    def _order(self, token, token_amount, order_type, type, limit=None):
        # If token is not in wallet, initialize it
        if not token in self.wallet:
            self.wallet.update({token: 0})

        # Validate 
        if type == 'buy' and Decimal(token_amount) > self.wallet['stable']:
            raise Exception('Not enough stable!')
        elif type == 'sell' and token_amount > self.wallet[token]:
            raise Exception(f"Not enough {token} in wallet!")

        if limit:
            print(f"Placed {order_type} {type} order for {round(token_amount, 4) if type == 'sell' else round(token_amount * Decimal(self.prices[token]), 4)} {token}{f' at {round(limit, 4)}' if limit else ''}")


        if type == 'buy' or 'sell' and order_type == 'market' or 'limit':
            obj = {'type': type, 'order_type': order_type, 'token': token, 'amount': token_amount}

            # If market order, prioritize and call immediatly
            if order_type == 'market':
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


                    

                        




