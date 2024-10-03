import requests
import csv

url = "https://api.frankfurter.app/latest"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    print(data)
else:
    print(f"Error: Unable to fetch data (status code: {response.status_code})")

conversion_rates = data['rates']
conversion_rates['EUR']= 1

buy_currency =input("Currency you would like to buy (EUR,GBP,PLN,USD):").upper()
buy_amount =int(input("Amount:"))
sell_currency = input("Currency you would to pay (EUR,GBP,PLN,USD):").upper()

# with open('exchange_rates.csv', mode="w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Currency', 'Rate'])
#     for currency, rate in conversion_rates.items():
#         writer.writerow([currency,rate])
print(conversion_rates)

def from_buy_to_sell(buy_currency,buy_amount,sell_currency):
    if buy_currency and sell_currency in conversion_rates:

        sell_amount = buy_amount * (1/conversion_rates[buy_currency]) * conversion_rates[sell_currency]

    return print(f"To buy {buy_amount}{buy_currency} you will need to pay {sell_amount:.2f}{sell_currency}.")

from_buy_to_sell()
