'''import requests
TOKEN = "163feb946049f9742fbf39ff0e5f463f79a9d0f7"#os.environ['TOKEN']


#auth
headers={'Authorization': 'Token {}'.format(TOKEN)}


data = {'uid': 'UCeLzT-7b2PBcunJplmWtoDg', 'live_title': '【テイルズオブシンフォニア】可愛い娘と旅にでよう！そうしよう！初見プレイだ！\u3000#3【周防パトラ / ハニスト】',
 'live_url': 'https://www.youtube.com/watch?v=sl325qqk34I'}

url = 'https://vtuber-livestatus-api.herokuapp.com/api/onlive'
res = requests.post(url, data, headers=headers)

print(res)'''

uid = 'UCL34fAoFim9oHLbVzMKFavQ'

#import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os, time
from tqdm import tqdm
import threading

BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' #heroku

#get request, return=json data
def get(URL):
   return requests.get(URL).json()

#channel idを受け取って放送中の場合は配信場所のURL、そうでない場合はFalseを返す
def live_status(channelid):
    youtube_url = "https://www.youtube.com"
    channel_site_url = youtube_url + "/channel/"
    channel_site_url += channelid
    hed = {'Accept-Language': 'ja'}
    html_data = requests.get(channel_site_url, headers=hed)
    parsed = bs4.BeautifulSoup(html_data.content, "html.parser")
    print(parsed)


live_status(uid)