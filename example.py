import requests
import time 
import json
from bs4 import BeautifulSoup as bs

url = 'http://m.exchange.daum.net/mobile/exchange/exchangeMain.daum'
response = requests.get(url).text
soup = bs(response, 'html.parser')

li = soup.select('.name')

lists = []
count = 0
for i in li:
    list = {
        "country" : i.select_one('a').text,
        
        "exch" : soup.select('.idx')[count].text
    }
    lists.append(list)
    count+=1
print(lists)