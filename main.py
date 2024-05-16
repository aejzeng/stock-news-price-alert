import requests
import datetime as dt
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_api_key = "HCGINWMCJUQU7YMA"
stock_endpoint = "https://www.alphavantage.co/query"
news_api_key = "b214722829974aa18e6b9cb73948a489"
news_endpoint = "https://newsapi.org/v2/everything"
stock_function = "TIME_SERIES_DAILY"

stock_parameters = {
    "function": stock_function,
    "symbol": STOCK,
    "apikey": stock_api_key
}

# today = dt.datetime.now()
# yesterday = today - dt.timedelta(days=1)
# day_before_yesterday = today - dt.timedelta(days=2)

# yesterday_str = yesterday.strftime("%Y-%m-%d")
# day_before_yesterday_str = day_before_yesterday.strftime("%Y-%m-%d")


response = requests.get(url=stock_endpoint, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]

#Get a hold of price info direclty in each of dates' prices
formatted_stock_price = [value for (key, value) in stock_data.items()]
today_price = formatted_stock_price[0]["4. close"]  #As a string data type
yesterday_price = formatted_stock_price[1]["4. close"]
print(today_price)
print(yesterday_price)

#Calculate the percentage change
price_diff = float(yesterday_price) - float(today_price)

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
up_down = None
if price_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percentage = round((price_diff / float(yesterday_price)) * 100, 1)

if abs(diff_percentage) > 0:

    news_parameters = {
        "apikey": news_api_key,
        "qInTitle": COMPANY_NAME,
        "language": "en"
    }

    news_response = requests.get(url=news_endpoint, params=news_parameters)
    news_response.raise_for_status()

    news_data = news_response.json()

    articles = news_data["articles"]

    # STEP 2: Use https://newsapi.org    Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    three_articles = articles[:3]
    formatted_three_articles_list = [f"{COMPANY_NAME}: {up_down}{diff_percentage}%\nHeadlines: {article['title']} \nBrief: {article['description']}" for article in
                                     three_articles]

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.
    account_sid = "AC3e137c4b52191eefe694bc3152f22ecd"
    auth_token = "10fbab13b0fb7f2d8fa1e1f6bbb55eca"

    client = Client(account_sid, auth_token)

    for article in formatted_three_articles_list:
        message = client.messages.create(
            from_="+15078734364",
            body=article,
            to="+4917684482519"
        )
        print(formatted_three_articles_list)
        print(message.status)

# try:
#     yesterday_str = yesterday.strftime("%Y-%m-%d")
#     day_before_yesterday_str = day_before_yesterday.strftime("%Y-%m-%d")
#
#     yesterday_price = float(stock_data["Time Series (Daily)"][yesterday_str]["4. close"])
#     day_before_yesterday_price = float(stock_data["Time Series (Daily)"][day_before_yesterday_str]["4. close"])
#
#     #Calculate the percentage change
#     percentage_change = ((yesterday_price - day_before_yesterday_price) / yesterday_price) * 100
#
#     if abs(percentage_change) >= 5:
#         get_news()
#
# except KeyError as e:
#     print(f"Error: {e} data not available in the stock price JSON file.")




