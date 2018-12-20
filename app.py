from flask import Flask, render_template, request
import time
import requests
import json
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

today = time.strftime("%a").lower()

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/lotto')
def lotto():
    return render_template('lotto.html')
    
@app.route('/toon')
def toon():
    cat = request.args.get('type')
    if(cat == 'naver'):
        url = 'https://comic.naver.com/webtoon/weekdayList.nhn?week=' + today
        response = requests.get(url).text
        soup = bs(response, 'html.parser')
    
        toons = []
        li = soup.select('.img_list li')
        for item in li:
          toon = {
            "title" : item.select_one('dt a').text, 
            "url" : 'https://comic.naver.com' + item.select('dt a')[0]["href"],
            "img_url" : item.select('.thumb img')[0]["src"]
          }
          toons.append(toon)
          
    elif (cat == 'daum'):

        url = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/' + today
        response = requests.get(url).text
        document = json.loads(response)
        data = document["data"]
        print(data)
        
        toons = []
        
        for toon in data:
          toon = {
            "title" : toon["title"], 
            "url" : 'http://webtoon.daum.net/webtoon/view/' + toon["nickname"], 
            "img_url" : toon["pcThumbnailImage"]["url"]
          }
          toons.append(toon)
    
    return render_template('toon.html', cat = cat, t = toons)

@app.route('/apart')
def apart():
    # 1. 내가 원하는 정보를 얻을 수 있는 url을 url 변수에 저장한다.
    url = 'http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20331939&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode='
    # 1-1. request header에 추가할 정보를 dictionary 형태로 저장한다.
    headers = {
        "Host" : "rt.molit.go.kr", 
        "Referer": "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"
    }
    # 2. requests의 get 기능을 이용하여 해당 url에 header와 함께 요청을 보낸다.
    # 저쪽에서 받는 변수 이름도 headers
    response = requests.get(url, headers = headers).text
    print((response))
    # 3. 응답으로 온 코드의 형태를 살펴본다.(json/xml/html)
#    document = json.loads(response)
#    print(document)
    # for d in document["result"]:
    #     print(d["BLDG_NM"])
    return render_template('/apart.html')

@app.route('/exchange')
def exchange():
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

    return render_template('exchange.html', t = lists)
