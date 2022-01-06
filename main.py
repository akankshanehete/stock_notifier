import requests
import os
import datetime
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# getting data from alphavantage stock API
stock_parameters = {
    'apikey': '///////////////',
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': STOCK,
    'interval': '60min'
}
stock_response = requests.get(url='https://www.alphavantage.co/query', params=stock_parameters)
stock_data = stock_response.json()['Time Series (60min)']

# getting yesterdays and the day before yesterdays closing stock prices
today = datetime.date.today()
yesterday = datetime.date.today() - datetime.timedelta(1)
day_before_yesterday = datetime.date.today() - datetime.timedelta(2)
y_cl = float(stock_data[str(yesterday) + " 20:00:00"]['4. close'])
dby_cl = float(stock_data[str(day_before_yesterday) + " 20:00:00"]['4. close'])

# getting data from news API
news_parameters = {
    'apiKey': '///////////////',
    'q' : COMPANY_NAME,
    'from': str(yesterday),
    'to': str(today)
}

news_data = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters).json()
print(news_data)


# function checks the percent change between 2 values
def check_percent_change(initial_value, final_value):
    percent_chg = ((final_value - initial_value)/initial_value) * 100
    return int(percent_chg)

print(y_cl, dby_cl)
print(check_percent_change(dby_cl, y_cl))

# when stock price increases/decreases by 5% or more b/w yesterday and the day before yesterday,
# news articles are fetched for that company
if check_percent_change(dby_cl,y_cl) >= 5 and check_percent_change(dby_cl,y_cl) <= -5:
    print("Get News!")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
