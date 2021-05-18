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
        alert = bot.alerts[-1]
        ema4 = alert['4ma']
        token = alert['token']
        stable_balance = bot.wallet['stable']

        # Make sure bot has current price 
        if not token in bot.prices:
            continue
        
        current_price = Decimal(bot.prices[token])
        bot.alerts.pop()

        if bot.wallet['stable'] > 10:
            if ema4 == sorted(ema4):
                stop_loss = current_price - current_price * Decimal(0.01)
                stop_gain = current_price + current_price * Decimal(0.01)

                bot.market_buy(token, bot.wallet['stable'])
                bot.limit_sell(token, bot.wallet[token], stop_loss)
                bot.limit_sell(token, bot.wallet[token], stop_gain)
                #bot.limit_buy(token, bot.wallet['stable'], current_price + current_price * Decimal(0.01))
                #bot.trailing_stop_loss(token, bot.wallet[token], current_price, 0.002)
                

         
