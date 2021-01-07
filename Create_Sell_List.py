import datetime as dt
import yfinance as yf
import pandas_datareader as pdr


yf.pdr_override()

ema_short = 8
ema_long = 50

now = dt.datetime.now()
start = dt.datetime(now.year - 1, now.month + 9, now.day)

def create_sell_list(api, owned_symbol_list):
    # Create a list of symbols that are already being sold and exclude them.
    existing_sell_order_list = []
    orders = api.list_orders()

    rwb_is_false_list = []
    for symbol in owned_symbol_list:
        if symbol not in existing_sell_order_list:
            try:
                print(symbol)
                price = api.get_last_trade(symbol).price
                df = pdr.get_data_yahoo(symbol, start, now)

                # create new columns with ema ranges

                df["ema_8"] = round(df.iloc[:, 5].ewm(span=8, adjust=False).mean(),2)
                df["ema_50"] = round(df.iloc[:, 5].ewm(span=50, adjust=False).mean(),2)

                today_short_ema = df['ema_8'][-1]
                today_long_ema = df['ema_50'][-1]
                print(price, today_short_ema)

                # This is the threshold to suggest moving into a buy position for whatever stock meets this condition
                if price < today_short_ema:
                    rwb_is_false_list.append(symbol)

            except:
                pass
    return rwb_is_false_list

