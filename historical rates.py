import requests
import csv
buy_currency = "eur".upper()
pay_currency = "pln".upper()
start_date = "2024-09-01"
def historical_rates_for_plot (plot_currency,base_currency,start_date):
    url = f"https://api.frankfurter.app/{start_date}..?base={base_currency}&symbols={plot_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        historical_rates = data['rates']
        print(historical_rates)
        with open('historical_rates.csv', mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Rate'])
            for date ,rates in historical_rates.items():
                rate=rates[buy_currency]
                writer.writerow([date,rate])
    else:
        return print(f"Error: Unable to fetch data (status code: {response.status_code})")

historical_rates_for_plot(buy_currency,pay_currency,start_date)