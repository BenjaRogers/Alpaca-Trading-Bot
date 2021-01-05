import datetime as dt
import pandas_datareader as pdr
import yfinance as yf

def create_sell_order(api, symbol, time_in_force):
    price = api.get_last_trade(symbol).price
    limit_price = price * .99
    qty = api.get_position(symbol).qty
    api.submit_order(side='sell',
                     symbol=symbol,
                     type='limit',
                     limit_price=limit_price,
                     qty=qty,
                     time_in_force=time_in_force)