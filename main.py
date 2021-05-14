import threading, time
from decimal import *
from client import *   
fees = {"spot": Decimal(0.001), "market": Decimal(0.005)}

# Trading bot
class trading_bot():
    def __init__(self, fees, starting_amount):
        self.fees = fees
        self.alerts = []
        self.orders = []
        self.trades = []
        self.prices = {}
        self.wallet = {'stable': Decimal(starting_amount)}
        self.start()

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
        print(f"Executed market buy order for {new_amount} {token} at {self.prices[token]} ( ${stable_amount} )")
        self.trades.append({'type': 'buy', 'token': token, 'tokens_gained': new_amount, 'stable_lost': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})

    def exec_stop_loss(self, token, current_price, percent_below):
        pass
    
    def exec_trailing_stop_loss(self, token, current_price, percent_below):
        pass

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
        print(f"Executed market sell order for {token_amount} {token} at {self.prices[token]} ( ${stable_amount_after_fees} )")
        self.trades.append({'type': 'sell', 'token': token, 'tokens_lost': token_amount, 'stable_gained': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})

    def start(self):
        # Initialize client
        thread = threading.Thread(target=websocket_client, args=('ws://localhost:5000', self.prices, self.alerts))
        thread.start()
        
        time.sleep(5)
        self.market_buy("DOGEUSDT", 1000)
        self.market_sell("DOGEUSDT", self.wallet['DOGEUSDT'])
        print(self.wallet)
        return

        # Start bot
        while True:
            print(self.prices)
            
bot = trading_bot(fees, 1000)


