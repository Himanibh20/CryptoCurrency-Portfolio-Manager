import requests
import json

api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=5&convert=USD&CMC_PRO_API_KEY=6647381739534aa5a58cc382d3efe6aa")

api = json.loads(api_request.content)

print("--------------------")
print("--------------------")

coins = [
   {
      "symbol": "BTC",
      "amount_owned": 2,
      "price_per_coin": 3200
   },
   {
      "symbol": "ETH",
      "amount_owned": 100,
      "price_per_coin": 2.05
   }
]

total_profit_loss = 0

for i in range(0,5):
    for coin in coins:
        if api["data"][i]["symbol"] == coin["symbol"]:
         total_paid = coin["amount_owned"] * coin["price_per_coin"]
         current_value = coin["amount_owned"] * api["data"][i]["quote"]["USD"]["price"]
         profit_loss_percoin = current_value - total_paid
         total_profit_loss = profit_loss_percoin - total_paid

         total_profit_loss = total_profit_loss + profit_loss_percoin


         print(api["data"][i]["name"] + " - " + api["data"][i]["symbol"])
         print("Price = $ {0:.2f}".format(api["data"][i]["quote"]["USD"]["price"])) 
         print("Amount Owned:",coin["amount_owned"])
         print("Total Amount Paid:",total_paid)
         print("Current Value: $ {0:.2f}".format(current_value))
         print("Profit/Loss: $ {0:.2f}".format(profit_loss_percoin))
         print("Total Profit/Loss: $ {0:.2f}".format(total_profit_loss)) 
         print("--------------------") 

print("Overall Profit/Loss: $ {0:.2f}".format(total_profit_loss))         

