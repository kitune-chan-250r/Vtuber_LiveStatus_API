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
    #print(parsed)


live_status(uid)

import asyncio
import aiohttp
import re
from tqdm import tqdm
import requests
import random
from bs4 import BeautifulSoup
import json


"""api_keys = ['AIzaSyAf6M7VIuXyfkZVnII_WNIXunbiN2Po0qU',
            'AIzaSyDc4eiGx2LJUFgdGI453NXnNpJwEzfbHHI',
            'AIzaSyBd_ljjcFJo5rC6IIh8IfztcCHc5OtTR24',
            'AIzaSyCB4efFgu8H0sIFl9u5CQttYh1Wdit0Ueg',
            'AIzaSyA0-ZTkYVrSwME51qtCNuv2lvsllw8fXX8',
            'AIzaSyBV8dDWpE41q32JYANzBwfoXtL-ZxTOiMU',
            'AIzaSyCs7S3OBW7F2U4v8Y5tTSuqzDJbI-8uVXo',
            'AIzaSyAP5ZIgh6gwjEKNndaZKRFRBkei2LrhJBo',
            'AIzaSyDCtEe4Cv_DmXPCN8oBa7v-zTd_xh7PPqg',
            'AIzaSyA-FV3AZuBBxXvCUNeUnWL1_sB5bcUpWIg',
            'AIzaSyCjtiTj08c2t86HB5T5XrGTFnzqOEjAFXQ',
            'AIzaSyCOXBSQxEKPCl0tyeOI4SqjaAirs2qo0Ew',
            'AIzaSyBp6hZ0qm99sxCPUPe6ir_8sjkBmueFEMM',
            'AIzaSyASyQPi9A5r6zJco4GS87gOcY4u80sCC1Q',
            'AIzaSyCsBEUIRLaRF7O6nRl7YC9zpzdAwUNaFk4',
            'AIzaSyDOdfML2WLRSZSq5ATKq4mH98MlqAf7cBk',
            'AIzaSyCfhWXZnPBrjQth3eI4FcnYn9p_rJyr-2E',
            'AIzaSyAJ8R_BfgNWQjiaFsgqRDi7OpKZRLxth1Q',
            'AIzaSyCJvydjvbUckYSP_vnMvlq-6mID29rs_Ms',
            'AIzaSyAroxsOf5nKtIL86G9pCU9zXtsOMkNU1p8',
            'AIzaSyCt50hyGXY6k3RDe195yM86ZLn4DV8Lmxg',
            'AIzaSyC4G1w1DAKAv2G6S7Lo8JECjM8Xka8H8TQ',
            'AIzaSyDCHtArBNvpKNAeqo4j8xsE_omXRHdJKN0',
            'AIzaSyBQ8SLkyNG7vwI9Ym6YRVcOjT8kimxyyXs',
            'AIzaSyC9PSHYKIyhwEJfszxxNYluvFSaLV0mJs4']

'''async def main(uid):
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    async with aiohttp.ClientSession(headers=hed) as session:
        async with session.get(url) as response:
            html = await response.text()
           
    return result'''
BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' 
api_main = 'https://www.googleapis.com/youtube/v3/'
search_channel = 'search?part=snippet&channelId='
channelID = 'UCQ0UDLQCjY0rmuxCDE38FGg'
#r = requests.get(api_main + search_channel + channelID + '&key=' + api_keys[0] + '&type=video&eventType=live')

all_liver = requests.get(BASE_URL).json()
uids = [liver['uid'] for liver in all_liver]

for uid in uids:
    keynumber = random.randint(0, 24)
    print(keynumber)
    key = api_keys[keynumber]
    print(key)
    r = requests.get(api_main + search_channel + uid + '&key=' + key + '&type=video&eventType=live').json()
    #r['']
    if r['items'] != []:
        result = {'watch': r['items'][0]['id']['videoId'], 'title': r['items'][0]['snippet']['title'], 'uid': uid, 'status': True}
    else:
        result = {'uid': uid, 'status': False}

    print(result)


"""

url = 'https://www.youtube.com/channel/UCSFCh5NL4qXrAy9u-u2lX3g'
res = requests.get(url).text
parsed = BeautifulSoup(res, "html.parser") #配信中２７


script1 = parsed.find_all('script', text=re.compile("ライブ配信中"))
script2 = parsed.find_all('script', text=re.compile("人が視聴中"))

#print(len(script2))

#


for scrp in parsed.find_all("script"):
    if "window[\"ytInitialData\"]" in scrp.text:
        dict_str = scrp.text.split(" = ")[1]

        # javascript表記なので更に整形. falseとtrueの表記を直す
        dict_str = dict_str.replace("false","False")
        dict_str = dict_str.replace("true","True")

        # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
        dict_str = dict_str.rstrip("  \n;")

        dict_str = dict_str.replace('    window["ytInitialPlayerResponse"]', '')
        dict_str = dict_str.replace(";", "")
        # 辞書形式に変換
        dics = eval(dict_str)
        break

stream_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                        ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][1]\
                        ['itemSectionRenderer']['contents'][0]\
                        ['shelfRenderer']['content']['expandedShelfContentsRenderer']['items'][0]\
                        ['videoRenderer']

watch = stream_description['videoId']
title = stream_description['title']['simpleText']
print(title)