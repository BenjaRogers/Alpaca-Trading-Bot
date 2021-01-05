import datetime as dt
import pandas_datareader as pdr
import yfinance as yf

#sample
# api.submit_order(symbol='QDEC',
#                      qty=10,
#                      side='buy',
#                      type='market',
#                      time_in_force='day')

yf.pdr_override()
now = dt.datetime.now()
start = dt.datetime(now.year, now.month, now.day-1)


def create_buy_order(api, symbol, time_in_force, order_class):

    # Initialize order variables.
    price = api.get_last_quote(symbol).bidprice  # set target price as alpaca API last_quote
    limit_buy_price = price * 1.01
    limit_price_profit = price * 1.1  # set target profit to 10 %
    stop_price = price * 0.96  # set stop loss to 4%
    limit_price_loss = price * 0.95
    qty = buy_amount(symbol, 200)

    print(f"Symbol: {symbol} \n"
          f"Last Quote: {price} \n"
          f"Take Profit Limit: {limit_price_profit} \n"
          f"Stop Loss: {stop_price} \n"
          f"Stop Limit: {limit_price_loss} \n"
          f"Quantity: {qty}")

    api.submit_order(side='buy',
                     symbol=symbol,
                     type='limit',
                     limit_price=limit_buy_price,
                     qty=qty,
                     time_in_force=time_in_force,
                     order_class=order_class,
                     take_profit={'limit_price':limit_price_profit},
                     stop_loss={'stop_price':stop_price,
                                'limit_price':limit_price_loss})

def buy_amount(stock_name, target):
    total = 0
    num = 0
    df = pdr.get_data_yahoo(stock_name, start, now)
    price = df.iloc[:, 5][-1]
    while total <= target:
            total += price
            num += 1

    return str(num)