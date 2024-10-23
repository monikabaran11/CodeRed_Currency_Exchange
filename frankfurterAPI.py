import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta
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

# def download_rates_to_csv(): # not used yet but might be used for future code.
#     with open('exchange_rates.csv', mode="w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Currency', 'Rate'])
#         for currency, rate in conversion_rates.items():
#             writer.writerow([currency,rate])
def from_buy_to_sell(buy_currency,buy_amount,pay_currency):

    if buy_currency in conversion_rates and pay_currency in conversion_rates:
        pay_amount = buy_amount * (1/conversion_rates[buy_currency]) * conversion_rates[pay_currency]
        return f"To Buy {buy_amount}{buy_currency} you will need to pay {pay_amount:.2f}{pay_currency}."
    else:
        return "Currency not supported"

def from_sell_to_buy(sell_currency, sell_amount, receive_currency):
    if sell_currency in conversion_rates and receive_currency in conversion_rates:
        receive_amount = sell_amount * (1/conversion_rates[sell_currency]) * conversion_rates[receive_currency]
        return f"If you Sell {sell_amount}{sell_currency} you will get {receive_amount:.2f}{receive_currency}."
    else:
        return "Currency not supported"


def historical_rates_for_plot (base_currency,plot_currency): #base_currency=from_currency,plot_currency =to_currency(quote currency),start_date= set for 6 month
    start_date = (datetime.now() - relativedelta(months=6)).date()
    start_date_str = str(start_date)
    print(f'Starting Point: {start_date_str}')
    url = f"https://api.frankfurter.app/{start_date_str}..?base={base_currency}&symbols={plot_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        historical_rates = data['rates']
        dates = []
        rate = []

        for date, rates in historical_rates.items():
            dates.append(date)
            rate.append(rates[plot_currency])
        df = pd.DataFrame({'Date': pd.to_datetime(dates), 'Rate': rate})  # changing format to datetime
        return df

    else:
        return print(f"Error: Unable to fetch data (status code: {response.status_code})")

def plot_historical_rates(base_currency,plot_currency,df):
    fig = px.line(df, x='Date', y='Rate', title=f'Historical rates for {base_currency}',labels={'Rate': f'Exchange Rate in ({base_currency}/{plot_currency})','Date': 'For last 6 months'})
    fig.add_hline(y=current_rate,line_color="Red",line_dash='dash', line_width=2, annotation_text=f'Current Rate({base_currency}/{plot_currency})', annotation_position="bottom right")
    fig.update_layout(showlegend=True)
    return fig.show()
def calculating_RSI(df_historical_rates):
    df_historical_rates['Daily_change'] = (df_historical_rates['Rate'].diff()).fillna(0)
    df_historical_rates['Positive'] = [x if x > 0 else 0 for x in df_historical_rates['Daily_change']]
    df_historical_rates['Negative'] = [x if x < 0 else 0 for x in df_historical_rates['Daily_change']]
    df_historical_rates['Positive_days'] = [1 if x > 0 else 0 for x in df_historical_rates['Positive']]
    df_historical_rates['Negative_days'] = [1 if x < 0 else 0 for x in df_historical_rates['Negative']]
    df_for_advise = df_historical_rates
    sum_positive = df_for_advise['Positive'].sum()
    sum_negative = -df_for_advise['Negative'].sum()
    sum_positive_days = df_for_advise['Positive_days'].sum()
    sum_negative_days = df_for_advise['Negative_days'].sum()
    average_profit = sum_positive / sum_positive_days
    average_loss = sum_negative / sum_negative_days
    RS = average_profit / average_loss
    RSI = 100 - (100 / (1 + RS))
    print(f'RSI {RSI:.5f} RSI>70 good to Sell, RSI<30 good to Buy')
    return RSI

def calculating_average_min_max_exchange_rate (df_historical_rates):
    average_ex_rate=df_historical_rates['Rate'].mean()
    max_ex_rate=df_historical_rates['Rate'].max()
    min_ex_rate=df_historical_rates['Rate'].min()
    print(f'Average rate {average_ex_rate:0.5f}')
    print(f'Highest rate{max_ex_rate}')
    print(f'Lowest rate {min_ex_rate}')


conversion_rates = download_conversion_rates()
while True:
    ex_direction = input("Do you want to Buy or Sell currency?.Provide B/S").upper()
    if ex_direction == "B":
        from_currency = input("Currency you would like to buy:").upper()
        ex_amount = int(input("Amount:"))
        to_currency = input("Currency you would to pay:").upper()
        exchange_statement = from_buy_to_sell(from_currency, ex_amount, to_currency)
        print(exchange_statement)
        if exchange_statement != "Currency not supported":
            break
    elif ex_direction == "S":
        from_currency = input("Currency you would like to sell:").upper()
        ex_amount = int(input("Amount:"))
        to_currency = input("Currency you would to receive:").upper()
        exchange_statement = from_sell_to_buy(from_currency, ex_amount, to_currency)
        print(exchange_statement)
        if exchange_statement != "Currency not supported":
            break
    else:
        print("Unrecognized choice of direction, please try once again")

investment_advise = (input("Do you want to see investment advise for your currency exchange order?'Provide Y/N").upper())

while True:
    if investment_advise == "Y":
        df_historical_rates = historical_rates_for_plot(from_currency,to_currency)
        current_rate = df_historical_rates['Rate'].iloc[-1]
        print(f'Current rate {current_rate:.5f} ({from_currency}/{to_currency})')
        calculating_RSI(df_historical_rates)
        calculating_average_min_max_exchange_rate(df_historical_rates)
        plot_historical_rates(from_currency,to_currency,df_historical_rates)
        break
    elif investment_advise == "N":
        break
    else:
        print("Unrecognized choice of direction, please try once again")






# based on current and historic data get the information about the trend of the rate and suggest if it is a good moment for an exchange of a given currency (or currencies)
# asking user if would like to see the trend plot for the pair of currencies chosen
