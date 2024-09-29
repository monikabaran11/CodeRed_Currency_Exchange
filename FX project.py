
buy_currency =input("Currency you would like to buy (EUR,GBP,PLN,USD):").upper()
buy_amount =int(input("Amount:"))
sell_currency = input("Currency you would to pay (EUR,GBP,PLN,USD):").upper()
eur_to_pln_rate = 4.27
eur_to_gbp_rate = 0.83
eur_to_usd_rate = 1.12

def from_buy_to_sell():
    if buy_currency == "EUR":
        if sell_currency == "PLN":
            sell_amount = buy_amount * eur_to_pln_rate
        elif sell_currency == "GBP":
            sell_amount = buy_amount * eur_to_gbp_rate
        elif sell_currency == "USD":
            sell_amount = buy_amount * eur_to_usd_rate
    elif buy_currency == "GBP":
       if sell_currency == "PLN":
           sell_amount= buy_amount*(1/eur_to_gbp_rate)*eur_to_pln_rate
       elif sell_currency == "USD":
           sell_amount= buy_amount*(1/eur_to_gbp_rate)*eur_to_usd_rate
       elif sell_currency == "EUR":
           sell_amount = buy_amount*(1/eur_to_gbp_rate)
    elif buy_currency == "USD":
        if sell_currency == "PLN":
            sell_amount = buy_amount * (1 / eur_to_usd_rate) * eur_to_pln_rate
        elif sell_currency == "GBP":
            sell_amount = buy_amount * (1 / eur_to_usd_rate) * eur_to_gbp_rate
        elif sell_currency == "EUR":
            sell_amount = buy_amount * (1 / eur_to_usd_rate)
    elif buy_currency == "PLN":
        if sell_currency == "USD":
            sell_amount = buy_amount * (1 / eur_to_pln_rate) * eur_to_usd_rate
        elif sell_currency == "GBP":
            sell_amount = buy_amount * (1 / eur_to_pln_rate) * eur_to_gbp_rate
        elif sell_currency == "EUR":
            sell_amount = buy_amount * (1 / eur_to_pln_rate)
    else:

        print("Incorrect input, please try once again")
    return print(f"To buy {buy_amount}{buy_currency} you will need to pay {sell_amount:.2f}{sell_currency}.")


from_buy_to_sell()