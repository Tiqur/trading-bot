import threading, time
from decimal import *
from client import *   
fees = {"spot": Decimal(0.01), "market": Decimal(0.05)}

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
        new_amount = prev_amount + stable_amount_after_fees * Decimal(self.prices[token])

        # Update wallet
        self.wallet[token] = new_amount
        self.wallet['stable'] -= stable_amount
        print(f"Executed market buy order for {new_amount} {token} at {self.prices[token]} ( ${stable_amount} )")
        self.trades.append({'token': token, 'amount': new_amount, 'cost': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})
        print(self.trades)

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

        # Calculate balance
        new_token_amount = self.wallet[token] - token_amount

        # Update wallet
        self.wallet[token] -= new_token_amount
        self.wallet['stable'] += stable_amount_after_fees
        print(f"Executed market sell order for {token_amount} {token} at {self.prices[token]} ( ${stable_amount} )")
        self.trades.append({'token': token, 'amount': token_amount, 'cost': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})
        print(self.trades)

    def start(self):
        # Initialize client
        thread = threading.Thread(target=websocket_client, args=('ws://localhost:5000', self.prices, self.alerts))
        thread.start()
        
        time.sleep(8)
        print(self.wallet)
        self.market_buy("DOGEUSDT", 1000)
        print(self.wallet)
        self.market_sell("DOGEUSDT", 10)
        print(self.wallet)
        return

        # Start bot
        while True:
            print(self.prices)
            
bot = trading_bot(fees, 1000)


