import requests
import json
# 환경변수에서 토큰 뽑아오기
import os

# 환경변수로부터 값을 가지고 온다!
token = os.getenv('TELEGRAM_TOKEN')
#url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
url = 'https://api.hphk.io/telegram/bot{}/getUpdates'.format(token)
#딕셔너리 형태로 만들어주기 위해서 json으로 바꾸어줌
response = json.loads(requests.get(url).text)
print(response)
url = 'https://api.hphk.io/telegram/bot{}/sendMessage'.format(token)
"""
"message":{
    "message_id":2,
    "from":{
        "id":706250897,
        "is_bot":false,
        "first_name":"\uc815\ud654",
        "last_name":"\ucd5c",
        "language_code":"ko"
        },
    "chat":{
        "id":706250897,
        "first_name":"\uc815\ud654",
        "last_name":"\ucd5c",
        "type":"private"
        },
    "date":1545283474,
    "text":"a"
    
"""
chat_id = response["result"][-2]["message"]["from"]["id"]
msg = response["result"][-2]["message"]["text"]

requests.get(url, params = {"chat_id": chat_id, "text": msg})