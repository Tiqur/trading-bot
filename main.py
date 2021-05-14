import threading, time
from decimal import *
from trading_bot import *
fees = {"spot": Decimal(0.001), "market": Decimal(0.005)}
starting_amount = 1000

# Initialize new bot
bot = TradingBot(fees, starting_amount)

time.sleep(4)
bot.market_buy("DOGEUSDT", 1000)
print(bot.wallet)

# Custom rules
while True:
    # Manage alerts
    if bot.alerts:
        alert = bot.alerts.pop()
        print(alert)


         
