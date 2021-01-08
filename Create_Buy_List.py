import datetime as dt
import yfinance as yf
import pandas_datareader as pdr


yf.pdr_override()

ema_short = 8
ema_long = 50

now = dt.datetime.now()
start = dt.datetime(now.year - 1, now.month + 9, now.day)

def create_buy_list(file, owned_symbol_list, active_order_list):

    file = open(file, 'r')
    string = file.read()
    string = string.strip("'")
    stock_list = string.split("', '")
    rwb_is_true_list = []
    len_list = len(stock_list)
    count = 0
    for symbol in stock_list:

        if symbol not in owned_symbol_list and symbol not in active_order_list:

            try:
                print(f"{count}/{len_list}")
                df = pdr.get_data_yahoo(symbol, start, now)

                # create new columns with ema ranges
                df["ema_8"] = round(df.iloc[:, 5].ewm(span=8, adjust=False).mean(),2)
                df["ema_50"] = round(df.iloc[:, 5].ewm(span=50, adjust=False).mean(),2)

                today_short_ema = df['ema_8'][-1]
                today_long_ema = df['ema_50'][-1]

                yesterday_short_ema = df['ema_8'][-2]
                yesterday_long_ema = df['ema_50'][-2]


                # This is the threshold to suggest moving into a buy position for whatever stock meets this condition
                if today_short_ema > today_long_ema and yesterday_short_ema < yesterday_long_ema:
                    rwb_is_true_list.append(symbol)
                    print(rwb_is_true_list)
            except:
                pass
        count += 1

    return rwb_is_true_list

