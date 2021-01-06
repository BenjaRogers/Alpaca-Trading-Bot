import alpaca_trade_api as tradeapi
import datetime as dt

######################################################################################
# Initialize API and account objects with key, secret key and paper account URL.
######################################################################################

key = "PKIUVBXXIYXDREPILOQY"
sec = "tZAgFZjMk0fFMrZUQy923hqou7HNrHgSD4KgLMEa"
url = "https://paper-api.alpaca.markets"

api = tradeapi.REST(key, sec, url, api_version='v2')
account = api.get_account()
