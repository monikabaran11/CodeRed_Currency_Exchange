import requests
import pandas as pd
import plotly.express as px
import csv
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
    print(f'Analysis starting point: {start_date_str}')
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
    return average_ex_rate, max_ex_rate, min_ex_rate

def recomendation_for_Buy(RSI,average_rate, max_rate, min_rate,current_rate):
    rec_statement= "Today’s Buy recommendation :"
    if RSI>=70 and current_rate >= average_rate:
        print(f'{rec_statement} Hold off, wait for market correction.\nCurrent rate is near the maximum rate : {max_rate} over the last six months')
    elif RSI<70 and current_rate >=average_rate:print(f'{rec_statement} Be patient, wait for better entry point.')
    elif RSI>30 and current_rate < average_rate:print(f'{rec_statement} Considering buying, but waiting is an option.')
    elif RSI<=30 and current_rate < average_rate:
        print(f'{rec_statement} Strong encourage to buy.\nCurrent rate is near the minimum rate : {min_rate} over the last six months')

def recomendation_for_Sell(RSI,average_rate, max_rate, min_rate,current_rate):
    rec_statement= "Today’s Sell recommendation :"
    if RSI>=70 and current_rate >= average_rate:
        print(f'{rec_statement} Strong encouragement to sell.\nCurrent rate is near the maximum rate: {max_rate} over the last six months')
    elif RSI<70 and current_rate >=average_rate:print(f'{rec_statement} Consider selling, but holding is an option')
    elif RSI>30 and current_rate < average_rate:print(f'{rec_statement} Be patient, wait for a stronger sell signal')
    elif RSI<=30 and current_rate < average_rate:
        print(f'{rec_statement} Hold off, wait for a price rebound.\nCurrent rate is near the minimum rate: {min_rate} over the last six months')

def rates_for_orders_check (start_date,base_currency,quote_currency): #
    url = f"https://api.frankfurter.app/{start_date}..?base={base_currency}&symbols={quote_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        historical_rates = data['rates']
        dates = []
        rate = []

        for date, rates in historical_rates.items():
            dates.append(date)
            rate.append(rates[quote_currency])
        df = pd.DataFrame({'Date': pd.to_datetime(dates), 'Rate': rate})  # changing format to datetime
        return df

    else:
        return print(f"Error: Unable to fetch data (status code: {response.status_code})")
def stop_order_check():  # not used yet but might be used for future code.
    so_df = pd.read_csv('Stop_order.csv', sep=',')
    so_date = str(so_df['Date'].iloc[0])
    print(f"Your stop order details\n{so_df}")
    so_rate = so_df['Stop Price'].iloc[0]
    so_base = str(so_df['From Currency'].iloc[0])
    so_quote = str(so_df['To Currency'].iloc[0])
    so_direction = str(so_df['Direction'].iloc[0])
    so_hist_rates_df = rates_for_orders_check(so_date,so_base,so_quote)
    hist_rate_list = so_hist_rates_df['Rate'].tolist()
    hist_date_list = so_hist_rates_df['Date'].tolist()
    i=0
    if so_direction == "S":
        while i<len(hist_rate_list):
            if hist_rate_list[i] <= so_rate:
                print(f"Your stop order has been executed on {hist_date_list[i]} after rate dropped to {hist_rate_list[i]}")
                break
            i+=1
        else: print("Your stop order is pending")
    elif so_direction == "B":
        while i<len(hist_rate_list):
            if hist_rate_list[i] >= so_rate:
                print(f"Your stop order has been executed on {hist_date_list[i]} after rate reached {hist_rate_list[i]}")
                break
            i+=1
        else:
            print("Your stop order is pending")
def limit_order_check():
    lim_df = pd.read_csv('Limit_order.csv', sep=',')
    lim_date = str(lim_df['Date'].iloc[0])
    print(f"Your limit order details\n{lim_df}")
    lim_rate = lim_df['Limit Price'].iloc[0]
    lim_base = str(lim_df['From Currency'].iloc[0])
    lim_quote = str(lim_df['To Currency'].iloc[0])
    lim_direction = str(lim_df['Direction'].iloc[0])
    lim_hist_rates_df = rates_for_orders_check(lim_date,lim_base,lim_quote)
    hist_rate_list = lim_hist_rates_df['Rate'].tolist()
    hist_date_list = lim_hist_rates_df['Date'].tolist()
    i=0
    if lim_direction == "S":
        while i<len(hist_rate_list):
            if hist_rate_list[i] >= lim_rate:
                print(f"Your limit order has been executed on {hist_date_list[i]} after rate reached {hist_rate_list[i]}")
                break
            i+=1
        else: print("Your limit order is pending")
    elif lim_direction == "B":
        while i<len(hist_rate_list):
            if hist_rate_list[i] <= lim_rate:
                print(f"Your limit order has been executed on {hist_date_list[i]} after rate dropped {hist_rate_list[i]}")
                break
            i+=1
        else:
            print("Your limit order is pending")



#0.Welcoming user + orders check for regular users
while True:
    print("Welcome to Forexpert !")
    first_time_user_check = input("Is this your first time here ? 'Provide Y/N").upper()
    if first_time_user_check == "Y":
        break
    elif first_time_user_check == "N":
        orders_check=input("Do you have any stop or limit order set with us that you would like to check? Y/N").upper()
        if orders_check =="Y":
            stop_order_check()
            limit_order_check()
            break
        elif orders_check=="N":
            break

        else:
            print("Unrecognized choice of direction, please try once again")

    else:
        print("Unrecognized choice of direction, please try once again")
#1.Retrieve a current rates, base ccurency EUR
conversion_rates = download_conversion_rates()

#2.Conversion based on the user needs
while True:
    ex_direction = input("Do you want to Buy or Sell currency?'Provide B/S").upper()
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

#3.Offering investment advise based on the historical rates and calulated parameters
investment_advise = (input("Do you want to see investment advise for your currency exchange order?'Provide Y/N").upper())

while True:
    if investment_advise == "Y":
        df_historical_rates = historical_rates_for_plot(from_currency, to_currency)
        current_rate = df_historical_rates['Rate'].iloc[-1]
        current_date = df_historical_rates['Date'].iloc[-1]
        print(f'Current rate {current_rate:.5f} ({from_currency}/{to_currency})')
        RSI=calculating_RSI(df_historical_rates)
        average_rate, max_rate, min_rate= calculating_average_min_max_exchange_rate(df_historical_rates)
        diff_current_max = current_rate - max_rate
        diff_current_min = current_rate - min_rate

        if diff_current_max > 0: print(f'Highest rate {max_rate} Current rate ↑ {diff_current_max:.5f}')
        elif diff_current_max == 0: print(f'Highest rate {max_rate} Current rate →')
        elif diff_current_max < 0: print(f'Highest rate {max_rate} Current rate ↓ {diff_current_max:.5f}')

        if diff_current_min > 0: print(f'Lowest rate {min_rate} Current rate ↑ {diff_current_min:.5f}')
        elif diff_current_min == 0: print(f'Lowest rate {min_rate} Current rate →')
        elif diff_current_min < 0: print(f'Lowest rate {min_rate} Current rate ↓ {diff_current_min:.5f}')

        if ex_direction == "B":
            print(recomendation_for_Buy(RSI, average_rate, max_rate, min_rate, current_rate))
        elif ex_direction == "S":
            print(recomendation_for_Sell(RSI, average_rate, max_rate, min_rate, current_rate))

        plot_historical_rates(from_currency, to_currency, df_historical_rates)
        break

    elif investment_advise == "N":
        break
    else:
        print("Unrecognized choice of direction, please try once again")

#4 Stop order and limit order
current_date= datetime.today().date()
limit_order = (input("Do you want to create a limit order for your currency pair ?'Provide Y/N").upper())
while True:
    if limit_order == "Y":
        limit_price = float(input("Please provide the limit order rate:"))
        with open('Limit_order.csv', mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date','Limit Price','From Currency','To Currency','Direction'])
            writer.writerow([current_date,limit_price,from_currency,to_currency,ex_direction])
        break
    elif limit_order == "N":
        break
    else:
        print("Unrecognized choice, please try once again")

stop_order = (input("Do you want to create the stop order for your currency pair ?'Provide Y/N").upper())
while True:
    if stop_order == "Y":
        stop_price = float(input("Please provide the stop order rate:"))
        with open('Stop_order.csv', mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'Stop Price', 'From Currency', 'To Currency', 'Direction'])
            writer.writerow([current_date, stop_price, from_currency, to_currency, ex_direction])
        break
    elif stop_order == "N":
        break
    else:
        print("Unrecognized choice of direction, please try once again")




# based on current and historic data get the information about the trend of the rate and suggest if it is a good moment for an exchange of a given currency (or currencies)
# asking user if would like to see the trend plot for the pair of currencies chosen
