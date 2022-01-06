import requests
import os
import datetime
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# getting data from alphavantage stock API
stock_parameters = {
    'apikey': '///////////',
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
    'apiKey': '//////////////',
    'q': COMPANY_NAME,
    'from': str(yesterday),
    'to': str(today)
}

# function checks the percent change between 2 values
def check_percent_change (initial_value, final_value):
    percent_chg = ((final_value - initial_value)/initial_value) * 100
    return int(percent_chg)

p_diff = check_percent_change(dby_cl, y_cl)

# twilio account information
account_sid = "ACfac3be954ae620d6aa6dfadc5b4d9e7c"
auth_token = "/////////////////"

# when stock price increases/decreases by 5% or more b/w yesterday and the day before yesterday,
# news articles are fetched for that company and text message is sent

if p_diff >= 5 and p_diff <= -5:
    news_data = requests.get(url='https://newsapi.org/v2/everything', params=news_parameters).json()['articles'][0:3]
    article1 = (news_data[0]['title'], news_data[0]['description'][0:100]+'...')
    article2 = (news_data[1]['title'], news_data[1]['description'][0:100]+'...')
    article3 = (news_data[2]['title'], news_data[2]['description'][0:100]+'...')
    if p_diff > 0:
        text_diff = '🔺' + str(p_diff)+'%'
    else:
        text_diff = '🔻' + str(p_diff)[1:2] + '%'
    message = "TSLA: " + text_diff + "\n Headline: " + article1[0]+"\n Brief: " + article1[1]
    # creating a client from the twilio API
    client = Client(account_sid, auth_token)
    # sending a rain message if it is going to rain that day
    message = client.messages.create(
        body= message,
        from_='+13233104492',
        to='+16477676905'
    )
else:
    print("not a significant stock change")
