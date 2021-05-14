import threading
from decimal import *
from trading_bot import *
fees = {"spot": Decimal(0.001), "market": Decimal(0.005)}
starting_amount = 1000

# Initialize new bot
bot = TradingBot(fees, starting_amount)
