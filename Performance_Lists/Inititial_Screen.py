import datetime as dt
from pandas_datareader import data as pdr
import yahoo_fin.stock_info as si
import pandas as pd

""" This script is to check how well a stock has performed over the last year based on Mark Minervini's conditions for 
    a strong stock. These 7 conditions are tested every day over the last year and a 'strength' is assigned to each stock
    based on how many of those days they met all 7 conditions. Stocks are then assigned to lists depending on how
    they performed. Each list is then put into a txt file for further use."""

now = dt.datetime.now()
start = dt.datetime(now.year - 2, now.month, now.day)

# For each possible position calculate simple moving  average @ the
# 50 day mark, the 150 day mark, and the 200 day mark. Additionally,
# calculate 52 week low and 52 week high.

# add range(len(stock_list))****
def initial_screen(stock_list):
    top_performers = []
    mid_high_performers = []
    mid_performers = []
    mid_low_performers = []
    low_performers = []
    stock_list = pd.read_csv(stock_list)

    for stock in stock_list.index:
        try:
            stock_name = stock_list['Name'][stock]
            pass_count = 0
            fail_count = 0
            df = pdr.get_data_yahoo(stock_name, start, now)
            DAYS = [50, 150, 200]

            # Adds new series to data frame for our 3 SMA variables we'll need
            for x in DAYS:
                sma = x
                df["sma_" + str(sma)] = round(df.iloc[:, 5].rolling(window=sma).mean(), 2)

            # Adds new series for min and max variables
            df["max"] = df["Adj Close"].rolling(window=255).max()
            df["min"] = df["Adj Close"].rolling(window=255).min()

            #initialize the variables we'll need for each day to check against conditions.
            for day in range(256, len(df.index)):

                simp_mov_avg_50 = df["sma_50"][day]
                simp_mov_avg_150 = df["sma_150"][day]
                simp_mov_avg_200 = df["sma_200"][day]
                close_price = df["Adj Close"][day]
                min = df["min"][day]
                max = df["max"][day]

                moving_average_200_20 = df["sma_200"][day-20]
                # print(simp_mov_avg_50, simp_mov_avg_150, simp_mov_avg_200, close_price, min, max)
                # file = open('chart_' + stock_list[stock] + '.txt', 'w')
                # file.write(df.to_string())
                # file.close()
                # Check against Mark Minervini's ** 7 conditions (Excluding the Relative Strength condition)
                # Check conditions each day for last year and calculate % of time the position satisfied all
                # 7 conditions.
                # Condition 1: Current Price > 150 SMA and > 200 SMA
                if simp_mov_avg_200 < close_price > simp_mov_avg_150:
                    cond_1 = True
                else:
                    cond_1 = False
                # Condition 2: 150 SMA > 200 SMA
                if simp_mov_avg_150 > simp_mov_avg_200:
                    cond_2 = True
                else:
                    cond_2 = False
                # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
                if simp_mov_avg_200 > moving_average_200_20:
                    cond_3 = True
                else:
                    cond_3 = False
                # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
                if simp_mov_avg_150 < simp_mov_avg_50 > simp_mov_avg_150:
                    cond_4 = True
                else:
                    cond_4 = False

                # Condition 5: Current Price > 50 SMA
                if close_price > simp_mov_avg_50:
                    cond_5 = True
                else:
                    cond_5 = False

                # Condition 6: Current Price is at least 30% above 52 week low
                # (Many of the best are up 100-300% before coming out of consolidation)
                if close_price >= min * 1.3:
                    cond_6 = True
                else:
                    cond_6 = False

                # Condition 7: Current Price is within 25% of 52 week high
                if close_price > max * 0.75:
                    cond_7 = True
                else:
                    cond_7 = False

                # Condition 8: IBD RS rating >70 and the higher the better ***********
                #
                #

                # If all conditions are met then pass count += 1. if all conditions then pass cont -= 1
                if cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7:
                    pass_count += 1
                else:
                    fail_count += 1
            try:
                pf_ratio = pass_count / fail_count
            except ZeroDivisionError:
                pf_ratio =  0

            if pf_ratio >= 1:
                top_performers.append(stock_name)
            if 0.75 <= pf_ratio < 1:
                mid_high_performers.append(stock_name)
            if 0.5 <= pf_ratio < 0.75:
                mid_performers.append(stock_name)
            if 0.25 <= pf_ratio < 0.5:
                mid_low_performers.append(stock_name)
            if 0.0 <= pf_ratio < .25:
                low_performers.append(stock_name)
            print(stock_name, pf_ratio, pass_count, fail_count)
        except:
            pass

    return top_performers, mid_high_performers, mid_performers, mid_low_performers, low_performers

top_performers = []
mid_high_performers = []
mid_performers = []
mid_low_performers = []
low_performers = []

top_performers, mid_high_performers, mid_performers, mid_low_performers, low_performers = initial_screen('tick_list_clean.csv')

print(top_performers)
print(mid_high_performers)
print(mid_performers)
print(mid_low_performers)
print(low_performers)

