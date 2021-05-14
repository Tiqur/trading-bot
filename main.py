import threading, time
from decimal import *
from trading_bot import *
fees = {"spot": Decimal(0.001), "market": Decimal(0.005)}
starting_amount = 1000

# Initialize new bot
bot = TradingBot(fees, starting_amount)

# Custom rules
while True:
    # Manage alerts
    if bot.alerts:
        alert = bot.alerts.pop()
        ema4 = alert['4ma']
        token = alert['token']
        print(alert)

        if bot.wallet['stable'] > 10:
            if ema4 == sorted(ema4):
                bot.market_buy(token, bot.wallet['stable'])
                bot.stop_loss(token, bot.wallet[token], bot.prices[token], 0.01)
                bot.trailing_stop_loss(token, bot.wallet[token], bot.prices[token], 0.02)
                

         
