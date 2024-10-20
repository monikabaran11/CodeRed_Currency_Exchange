import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
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
        return f"To Buy {buy_amount}{buy_currency} you will need to pay {pay_amount:.2f}{pay_currency}."
    else:
        return "Currency not supported"

def from_sell_to_buy(sell_currency, sell_amount, receive_currency, conversion_rates):
    if sell_currency in conversion_rates and receive_currency in conversion_rates:
        receive_amount = sell_amount * (1/conversion_rates[sell_currency]) * conversion_rates[receive_currency]
        return f"If you Sell {sell_amount}{sell_currency} you will get {receive_amount:.2f}{receive_currency}."
    else:
        return "Currency not supported"

start_date = "2024-03-01"
def historical_rates_for_plot (plot_currency,base_currency,start_date): #plot_currency =to_currency(quote currency), base_currency=from_currency
    url = f"https://api.frankfurter.app/{start_date}..?base={base_currency}&symbols={plot_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        historical_rates = data['rates']
        dates = []
        rate = []
        for date, rates in historical_rates.items():
            dates.append(date)
            rate.append(rates[plot_currency])
        df=pd.DataFrame({'Date': pd.to_datetime(dates),'Rate': rate}) # changing format to datetime
        current_rate = rate[-1]
        print(f'Current rate {current_rate}')
        df.describe()
        #plot 2
        # fig = px.line(df, x='Date', y='Rate', title=f'Historical rates for {base_currency}',labels={'Rate': f'Exchange Rate in ({base_currency}/{plot_currency})'})
        # fig.add_hline(y=current_rate,line_color="Red",line_dash='dash', line_width=2, annotation_text=f'Current Rate({base_currency}/{plot_currency})', annotation_position="bottom right")
        # fig.update_layout(showlegend=True)
        # fig.show()


    else:
        return print(f"Error: Unable to fetch data (status code: {response.status_code})")


conversion_rates = download_conversion_rates()
while True:
    ex_direction = input("Do you want to Buy or Sell currency?.Provide B/S").upper()
    from_currency = input("Currency you would like to buy:").upper()
    ex_amount = int(input("Amount:"))
    to_currency = input("Currency you would to pay:").upper()
    if ex_direction == "B":
        exchange_statement = from_buy_to_sell(from_currency, ex_amount, to_currency, conversion_rates)
        print(exchange_statement)
        if exchange_statement != "Currency not supported":
            break
    elif ex_direction == "S":
        exchange_statement = from_sell_to_buy(from_currency, ex_amount, to_currency, conversion_rates)
        print(exchange_statement)
        if exchange_statement != "Currency not supported":
            break
    else:
        print("Unrecognized choice of direction, please try once again")
historical_rates_for_plot(to_currency, from_currency, start_date)


