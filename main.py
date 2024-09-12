import requests
from datetime import datetime, timedelta
import time
from twilio.rest import Client

account_sid = ''
auth_token = ''

# --------------------- day calculation ----------------------


today = datetime.now()
formatted_today = today.strftime('%Y-%m-%d')

yesterday = today - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')

day_before_yesterday = today - timedelta(days=2)
formatted_day_before_yesterday = day_before_yesterday.strftime('%Y-%m-%d')

few_days_before = today - timedelta(days=30)

# Convert these dates to Unix timestamps
end_time = int(time.mktime(today.timetuple()))
start_time = int(time.mktime(few_days_before.timetuple()))

#  --------------------------STEP 1----------------


STOCK = "TSLA"
COMPANY_NAME = "IBM"
api_key = ""

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={COMPANY_NAME}&apikey={api_key}'
response = requests.get(url)
stock_data = response.json()

closing_price_yesterday = float(stock_data['Time Series (Daily)'][formatted_yesterday]['4. close'])
closing_price_day_before_yesterday = float(
    stock_data['Time Series (Daily)'][formatted_day_before_yesterday]['4. close'])

percentage_change = ((
                             closing_price_yesterday - closing_price_day_before_yesterday) / closing_price_day_before_yesterday) * 100

get_news = 0
if abs(percentage_change) >= 1:
    get_news = 1
else:
    print("Difference too small")


# ------------------------- STEP 2 --------------------------------


# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def fetch_data(start_date_time, end_date_time, media_type, query, language, skip, limit, token):
    url2 = 'https://dataapi.pavuk.ai/api/v1/data'
    params = {
        'startDateTime': start_date_time,
        'endDateTime': end_date_time,
        'mediaType': media_type,
        'query': query,
        'language': language,
        'skip': skip,
        'limit': limit
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response2 = requests.get(url2, headers=headers, params=params)
        response2.raise_for_status()
        data = response2.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    return []


if get_news == 1:
    news_data = fetch_data(
        start_date_time=start_time,
        end_date_time=end_time,
        media_type='News',
        query='IBM',
        language='english',
        skip=0,
        limit=3,
        token=''
    )

    message_body = f"IBM: {'🔺' if percentage_change > 0 else '🔻'}{abs(percentage_change):.2f}%\n"
    for news in news_data['data']:
        message_body += f"Headline: {news['title']}\n\n"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_="",
        to="",
    )

    print(message.status)



