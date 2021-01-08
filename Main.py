from Key import api, account
from Create_Buy_List import create_buy_list
from Create_Buy_Order import create_buy_order, buy_amount
from Create_Sell_List import create_sell_list
from Create_Sell_Order import create_sell_order
import time

def loop():
    # Get list of stocks that are already owned.
    position = api.list_positions()
    owned_position_list = []
    for i in range(len(position)):
        pos = position[i]
        owned_position_list.append(pos.symbol)

    # Get list of stocks that have been ordered but not filled.
    active_orders_list = []
    orders = api.list_orders()
    for order in orders:
        if order.side == 'buy' and order.status == 'new':
            orders.append(order.symbol)

    # Check top performers list for buys
    buy_order_list = create_buy_list("Performance_Lists/Top_Performers.txt", owned_position_list, active_orders_list)
    print("The following is a list of stocks that have recently crossed over: \n ", buy_order_list)

    # For each stock in buy_order_list create/submit a buy order to alpaca api
    for symbol in buy_order_list:
        # Determine how big of a position to take.
        # Submit buy order with bracket order_class -
        liquid_cash = float(account.cash)
        create_buy_order(api=api,
                         symbol=symbol,
                         time_in_force='day',
                         order_class='bracket',
                         cash=liquid_cash)

    # Check portfolio for positions where the current price has crossed below the short term ema
    sell_order_list = create_sell_list(api, owned_position_list)
    print("The following is a list of stocks to sell prior to meeting the take-profit or stop loss level \n",
          sell_order_list)
    for symbol in sell_order_list:
        create_sell_order(api=api,
                          symbol=symbol,
                          time_in_force='day')
    time.sleep(600)

def main():
    while True:
        if api.get_clock().is_open:
            loop()
        else:
            secs_to_open = api.get_clock().next_open - api.get_clock().timestamp
            if secs_to_open.total_seconds() < 7200:
                loop()
            else:
                time.sleep(60)

if __name__ == '__main__':
    main()