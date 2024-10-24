import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


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
        
        dates=[]
        rate=[]
        for date, rates in historical_rates.items():
            dates.append(date)
            rate.append(rates[plot_currency])
        df=pd.DataFrame({'Date': pd.to_datetime(dates),'Rate': rate}) # changing format to datetime
        current_rate=rate[-1]
        print(df)
        print(f'Current rate {current_rate}')

        #plot 1
        df.plot(x='Date', y='Rate', kind='line', figsize=(10, 6), title='historical exchange rates vs current rate')
        plt.show()
        
        #plot 2
        fig = px.line(df, x='Date', y='Rate', title='Historical rates',labels={'Rate': f'Exchange Rate ({plot_currency})'})
        fig.add_hline(y=current_rate,line_color="Red",line_dash='dash', line_width=2, annotation_text=f'Current Rate({plot_currency})', annotation_position="bottom right")
        fig.update_layout(showlegend=True)
        fig.show()


    else:
        return print(f"Error: Unable to fetch data (status code: {response.status_code})")

historical_rates_for_plot(buy_currency,pay_currency,start_date)



