import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import Vtuber_LiveStatus_API_lib as vlsa
from tqdm import tqdm
import datetime
import requests

#before update
"""async def main(uid):
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    async with aiohttp.ClientSession(headers=hed) as session:
        async with session.get(url) as response:
            html = await response.text()
            parsed = BeautifulSoup(html, "html.parser")
            
            element_1 = parsed.find_all("li", text=re.compile("ライブ配信中"))
            element_2 = parsed.find_all("li", text=re.compile("人が視聴中"))

            if len(element_1) > 0 and len(element_2) > 0:
                watch = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").attrs['href']
                title = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").text
                result = {'watch': watch.replace('/watch?v=', ''), 'title': title, 'uid': uid, 'status': True}
            else:
                result = {'uid': uid, 'status': False}
    return result

BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' 

all_liver = vlsa.get(BASE_URL)
on_liver = vlsa.get(BASE_URL + 'onlive/')
if len(on_liver) != 0:
    on_livers = [liver['uid']['uid'] for liver in on_liver]
else:
    on_livers = []

uids = [liver['uid'] for liver in all_liver]

loop = asyncio.get_event_loop()
done,pending = loop.run_until_complete(
    asyncio.wait([main(uid) for uid in tqdm(uids)]))

res = [d.result() for d in done] #結果
len(res)
for r in tqdm(res):
    #1つ前の更新で放送中ではなかったが返ってきたステータスが放送中だった場合
    if r['status'] is not False and r['uid'] not in on_livers:
        data = {'uid': r['uid'], 'live_title': r['title'],
                'live_url': 'https://www.youtube.com/watch?v='+r['watch']}
        #on_liveに追加
        print(data)
        res = vlsa.post(BASE_URL+'onlive', data)
    
    #1つ前の更新で放送中で返ってきたステータスも放送中だがタイトルが変わっていた場合
    #短期間に2度続けて放送するライバーに対応するための処理
    elif r['status'] is not False and r['uid'] in on_livers:
        title = [l['live_title'] for l in on_liver if l['uid']['uid'] == r['uid']]
        if r['title'] != title[0]:
            res = vlsa.delete(BASE_URL+'onlive', r['uid'])
            data = {'uid': r['uid'], 'live_title': r['title'],
                    'live_url': 'https://www.youtube.com/watch?v='+r['watch']}
            res = vlsa.post(BASE_URL+'onlive', data)
    
    #1つ前の更新で放送中で返ってきたステータスが放送中ではなかった場合
    elif r['status'] is False and r['uid'] in on_livers:
        res = vlsa.delete(BASE_URL+'onlive', r['uid'])"""
async def main(uid):
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    async with aiohttp.ClientSession(headers=hed) as session:
        async with session.get(url) as response:
            html = await response.text()
            parsed = BeautifulSoup(html, "html.parser")
            
            #element_1 = parsed.find_all('script', text=re.compile("ライブ配信中"))len(element_1) > 0 and 
            element_2 = parsed.find_all('script', text=re.compile("人が視聴中"))
            remind = parsed.find_all('script', text=re.compile("今後のライブ ストリーム"))
            
            result = {}
            result['onlive'] = {'uid': uid, 'status': False}

            if len(element_2) or len(remind) > 0:
                for scrp in parsed.find_all("script"):
                    if "var ytInitialData" in scrp.text:
                        dict_str = scrp.text.split(" = ")[1]

                        dict_str = dict_str.replace("false","False")
                        dict_str = dict_str.replace("true","True")

                        dict_str = dict_str.rstrip("  \n;")

                        dict_str = dict_str.replace('    window["ytInitialPlayerResponse"]', '')
                        dict_str = dict_str.replace(";", "")
                        
                        dics = eval(dict_str)
                        break

            if len(element_2) > 0:
                try:
                    '''2020-10-23 changed
                    stream_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                            ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]\
                                            ['itemSectionRenderer']['contents'][0]\
                                            ['channelFeaturedContentRenderer']['items'][0]\
                                            ['videoRenderer']'''
                    stream_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                            ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]\
                                            ['itemSectionRenderer']['contents'][0]\
                                            ['channelFeaturedContentRenderer']['items'][0]['videoRenderer']
                except KeyError:
                    result['onlive'] = {'uid': uid, 'status': False}

                else:
                    watch = stream_description['videoId']
                    audience = int(stream_description['viewCountText']['runs'][0]['text'].replace(',', ''))
                    
                    try:
                        #title = stream_description['title']['simpleText']
                        title = stream_description['title']['runs'][0]['text']
                    except KeyError:
                        title = "データ取得失敗 KeyError: stream_description['title']['simpleText']"

                    result['onlive'] = {'watch': watch, 'title': title, 'uid': uid, 'status': True, 'flag': 'onlive', 'audience': audience}

            elif len(remind) > 0:
                reminder_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                           ["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
                is_not_grid = True
                
                for rem in reminder_description:
                    if '今後のライブ ストリーム' in str(rem):
                        #print(reminder_description)
                        try:
                            contents = rem['itemSectionRenderer']['contents'][0]\
                                        ['shelfRenderer']["content"]['expandedShelfContentsRenderer']['items']
                        except KeyError:
                            contents = rem['itemSectionRenderer']['contents'][0]\
                                      ['shelfRenderer']["content"]['horizontalListRenderer']['items']
                            is_not_grid = False
                        
                        for reminds in contents:
                            #reminds = reminds['videoRenderer']#['videoRenderer']['gridVideoRenderer']
                            if is_not_grid:
                                reminds = reminds['videoRenderer']
                            else:
                                reminds = reminds['gridVideoRenderer']
                            reminder_watch = reminds['videoId']
                            reminder_title = reminds['title']['simpleText']
                            reminder_date = reminds['upcomingEventData']['startTime'] #UNIX time
                            try:
                                audience = reminds['shortViewCountText']['runs'][0]['text']
                            except KeyError:
                                audience = 0
                            result['reminder'] = {'watch': reminder_watch, 'title': reminder_title,
                                                  'uid': uid,'start_datetime': reminder_date, 'audience': audience, 'flag': 'reminder'}

                            break
            else:
                result['onlive'] = {'uid': uid, 'status': False, 'flag': 'onlive'}
    return result

def postTransaction(uid, res):
    liver_data = [x for x in all_liver if x['uid'] == uid][0]
    if uid in on_livers:
        startdatetime = [x['start_time'] for x in on_liver if x['uid']['uid'] == uid][0]
    else:
        startdatetime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    transaction = {
        'liver': str(liver_data),
        'title': res['title'],
        'startdatetime': startdatetime,
        'stream_url' : 'https://www.youtube.com/watch?v='+res['watch'],
        'onair': True,
        'audience': res['audience']
    }
    requests.post(Blockchain_URL+'transaction/', transaction)


BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' 
Blockchain_URL = 'https://vtuber-live-blockchain.herokuapp.com/'

all_liver = vlsa.get(BASE_URL + 'vtuber/')
on_liver = vlsa.get(BASE_URL + 'onlive/')


if len(on_liver) != 0:
    on_livers = [liver['uid']['uid'] for liver in on_liver]
else:
    on_livers = []

uids = [liver['uid'] for liver in all_liver]


loop = asyncio.get_event_loop()
done,pending = loop.run_until_complete(
    asyncio.wait([main(uid) for uid in uids]))

res = [d.result() for d in done] #結果

reminder = vlsa.get(BASE_URL + 'reminder')

#reminder all reset
for remind in reminder:
    res_reminder = vlsa.delete(BASE_URL+'reminder', remind['uid'])
    
#transaction送信用
for n in res:
    if n['onlive']['status'] == True:
        postTransaction(n['onlive']['uid'], n['onlive'])
requests.get(Blockchain_URL+'mining/')

for r in res:
    #1つ前の更新で放送中ではなかったが返ってきたステータスが放送中だった場合
    if r['onlive']['status'] is not False and r['onlive']['uid'] not in on_livers:
        r = r['onlive']
        data = {'uid': r['uid'], 'live_title': r['title'],
                'live_url': 'https://www.youtube.com/watch?v='+r['watch']}
        #on_liveに追加
        print(data)
        res = vlsa.post(BASE_URL+'onlive', data)
    
    #1つ前の更新で放送中で返ってきたステータスも放送中だがタイトルが変わっていた場合
    #短期間に2度続けて放送するライバーに対応するための処理
    elif r['onlive']['status'] is not False and r['onlive']['uid'] in on_livers:
        r = r['onlive']
        title = [l['live_title'] for l in on_liver if l['uid']['uid'] == r['uid']]
        if r['title'] != title[0]:
            res = vlsa.delete(BASE_URL+'onlive', r['uid'])
            data = {'uid': r['uid'], 'live_title': r['title'],
                    'live_url': 'https://www.youtube.com/watch?v='+r['watch']}
            res = vlsa.post(BASE_URL+'onlive', data)
    
    #1つ前の更新で放送中で返ってきたステータスが放送中ではなかった場合
    elif r['onlive']['status'] is False and r['onlive']['uid'] in on_livers:
        r = r['onlive']
        res = vlsa.delete(BASE_URL+'onlive', r['uid'])

    #ここからreminder
    elif 'reminder' in r:
        r = r['reminder']
        date = datetime.datetime.fromtimestamp(int(r['start_datetime']), datetime.timezone(datetime.timedelta(hours=9)))
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        gap = date - now
        if int(gap.days) < 1:
            data = {'uid': r['uid'], 'start_datetime': r['start_datetime'], 'live_title': r['title'],
                    'live_url': 'https://www.youtube.com/watch?v='+r['watch'], 'audience': r['audience']} #'uid', 'start_datetime', 'live_title', 'live_url', 'audience'
            res = vlsa.post(BASE_URL+'reminder', data)



