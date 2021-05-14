import threading, time
from decimal import *
from client import *   
fees = {"spot": 0.01, "market": 0.05}

# Trading bot
class trading_bot():
    def __init__(self, fees, starting_amount):
        self.fees = fees
        self.alerts = []
        self.orders = []
        self.trades = []
        self.prices = {}
        self.wallet = {'stable': starting_amount}
        self.start()

    def market_buy(self, token, stable_amount):
        if not token in self.prices:
            raise Exception(f"Token: {token} does not exist!")

        if stable_amount > self.wallet['stable']:
            raise Exception(f"Trade cannot exceed {self.prices['stable']} stable")

        stable_amount_after_fees = stable_amount - (stable_amount * self.fees['market'])

        # If token doesn't exist in wallet, create and initialize with a balance of 0
        if not token in self.wallet:
            self.wallet.update({token: 0})

        # Calculate balance
        prev_amount = self.wallet[token]
        new_amount = prev_amount + Decimal(stable_amount_after_fees) * Decimal(self.prices[token])

        # Update wallet
        self.wallet[token] = new_amount
        self.wallet['stable'] -= stable_amount
        print(f"Executed market order for {new_amount} {token} at {self.prices[token]} ( ${stable_amount} )")
        self.trades.append({'token': token, 'amount': new_amount, 'cost': stable_amount_after_fees, 'fees': (stable_amount * self.fees['market'])})
        print(self.trades)

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
        
        time.sleep(8)
        print(self.prices)
        self.market_buy("DOGEUSDT", 1000)
        return

        # Start bot
        while True:
            print(self.prices)
            
bot = trading_bot(fees, 1000)


