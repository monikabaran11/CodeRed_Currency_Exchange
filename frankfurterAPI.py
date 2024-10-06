import requests
import csv
def download_conversion_rates():
    url = "https://api.frankfurter.app/latest"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        conversion_rates = data['rates']
        conversion_rates['EUR'] = 1 #adding rate for EUR for calc.
        return conversion_rates
    else:
        return print(f"Error: Unable to fetch data (status code: {response.status_code})")
def download_rates_to_csv(): # not used yet but might be used for future code.
    with open('exchange_rates.csv', mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Currency', 'Rate'])
        for currency, rate in conversion_rates.items():
            writer.writerow([currency,rate])
def from_buy_to_sell(buy_currency,buy_amount,pay_currency,conversion_rates):

    if buy_currency in conversion_rates and pay_currency in conversion_rates:
        pay_amount = buy_amount * (1/conversion_rates[buy_currency]) * conversion_rates[pay_currency]
        return print(f"To Buy {buy_amount}{buy_currency} you will need to pay {pay_amount:.2f}{pay_currency}.")
    else :
        print("Currency not supported")

def from_sell_to_buy(sell_currency, sell_amount, receive_currency, conversion_rates):
    if sell_currency in conversion_rates and receive_currency in conversion_rates:
        receive_amount = sell_amount * (1/conversion_rates[sell_currency]) * conversion_rates[receive_currency]
        return print(f"If you Sell {sell_amount}{sell_currency} you will get {receive_amount:.2f}{receive_currency}.")
    else :
        print("Currency not supported")


conversion_rates = download_conversion_rates()
while True:
    ex_direction = input("Do you want to Buy or Sell currency?.Provide B/S").upper()
    if ex_direction == "B":
        buy_currency = input("Currency you would like to buy:").upper()
        buy_amount = int(input("Amount:"))
        pay_currency = input("Currency you would to pay:").upper()

        final_statement=from_buy_to_sell(buy_currency, buy_amount, pay_currency, conversion_rates)
        break
    elif ex_direction == "S":
        sell_currency = input("Currency you would like to sell:").upper()
        sell_amount = int(input("Amount:"))
        receive_currency = input("Currency you would to receive:").upper()

        final_statement=from_sell_to_buy(sell_currency, sell_amount, receive_currency, conversion_rates)
        break
    else:
        print("Unrecognized choice of direction, please try once again")


