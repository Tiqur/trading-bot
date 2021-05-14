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

    def market_buy(self, token, stable_amount):
        # If specified token does not exist
        if not token in self.prices:
            raise Exception(f"Token: {token} does not exist!")

        # If stable wallet ballance is insufficent
        if stable_amount > self.wallet['stable']:
            raise Exception(f"Trade cannot exceed {self.prices['stable']} stable")
        
        # Calculate stable amount after fees
        stable_amount_after_fees = stable_amount - (stable_amount * self.fees['market'])

        # If token doesn't exist in wallet, create and initialize with a balance of 0
        if not token in self.wallet:
            self.wallet.update({token: 0})

        # Calculate balance
        prev_amount = self.wallet[token]
        new_amount = prev_amount + stable_amount_after_fees / Decimal(self.prices[token])

        # Update wallet
        self.wallet[token] = new_amount
        self.wallet['stable'] -= stable_amount

        self.trades.append({'type': 'buy', 'token': token, 'tokens_gained': new_amount, 'stable_lost': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})
        print(f"Executed market buy order for {new_amount} {token} at {self.prices[token]} ( ${stable_amount} )")

    def market_sell(self, token, token_amount):
        # If specified token does not exist
        if not token in self.prices:
            raise Exception(f"Token: {token} does not exist!")

        # If token wallet ballance is insufficent
        if token_amount > self.wallet[token]:
            raise Exception(f"Trade cannot exceed {self.prices[token]} {token}")
        
        # Calculate stable amount after fees
        stable_amount = Decimal(self.prices[token]) * token_amount
        stable_amount_after_fees = stable_amount - (stable_amount * self.fees['market'])

        # Update wallet
        self.wallet[token] -= token_amount
        self.wallet['stable'] += stable_amount_after_fees

        self.trades.append({'type': 'sell', 'token': token, 'tokens_lost': token_amount, 'stable_gained': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})
        print(f"Executed market sell order for {token_amount} {token} at {self.prices[token]} ( ${stable_amount_after_fees} )")

    def stop_loss(self, token, amount, price, percent_below):
        self.orders.append({'type': 'stop_loss', 'token': token, 'amount': amount, 'price': price, 'percent_below': percent_below})
    
    def trailing_stop_loss(self, token, amount, price, percent_below):
        self.orders.append({'type': 'trailing_stop_loss', 'token': token, 'amount': amount, 'price': price, 'highest_price': price + price * percent_below, 'percent_below': percent_below})

    # Private sell method
    def _sell(self, token, new_token_amount, new_stable_amount):
        # update wallet
        self.wallet[token] -= new_token_amount
        self.wallet['stable'] += new_stable_amount

        # remove order
        self.orders.remove(order)

    def exec_loop(self):
        # Loop Executes orders and pops them off once filled
        while True:
            if self.orders:
                for order in self.orders:
                    type = order['type']
                    token = order['token']
                    amount = order['amount']
                    order_price = order['price']
                    percent_below = order['percent_below']
                    current_price = self.prices[token]
                    
                    # Calculate stable amount after fees
                    stable_amount = Decimal(current_price) * amount
                    stable_amount_after_fees = stable_amount - (stable_amount * self.fees['spot'])

                    # Loss
                    if type == 'stop_loss':
                        # Calculate threshold
                        threshold = order_price - order_price * percent_below

                        # If below 
                        if current_price < threshold:
                            self._sell(token, amount, stable_amount_after_fees)
                        
                    # Move threshold up if above threshold price
                    if type == 'trailing_stop_loss':
                        highest_price = order['highest_price']

                        if current_price > highest_price:
                            order['highest_price'] = current_price
            
                        trailing_threshold = highest_price - highest_price * percent_below


                        if current_price < trailing_threshold:
                            self._sell(token, amount, stable_amount_after_fees)





                        




