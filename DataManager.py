import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import Vtuber_LiveStatus_API_lib as vlsa
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

async def main(uid):
=======
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
from tqdm import tqdm

#before update
"""async def main(uid):
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    async with aiohttp.ClientSession(headers=hed) as session:
        async with session.get(url) as response:
            html = await response.text()
            parsed = BeautifulSoup(html, "html.parser")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
            
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD:DataManager.py
=======

>>>>>>> Stashed changes
            element_1 = parsed.find_all("li", text=re.compile("ライブ配信中"))
            #element_2 = parsed.find_all("li", text=re.compile("人が視聴中"))

            #if len(element_1) > 0 and len(element_2) > 0:
            if len(element_1) > 0:
                watch = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").attrs['href']
                title = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").text
                result = {'watch': watch.replace('/watch?v=', ''), 'title': title, 'uid': uid, 'status': True}
=======
=======
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======

>>>>>>> Stashed changes
            element_1 = parsed.find_all("li", text=re.compile("ライブ配信中"))
            element_2 = parsed.find_all("li", text=re.compile("人が視聴中"))

            #枠取り判定
            tmp_span = parsed.find('span', class_='branded-page-module-title-text')

            #枠取り判定
            tmp_span = parsed.find('span', class_='branded-page-module-title-text')

            if len(element_1) > 0 and len(element_2) > 0:
                watch = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").attrs['href']
                title = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").text
                result = {'watch': watch.replace('/watch?v=', ''), 'title': title, 'uid': uid, 'status': True}
<<<<<<< Updated upstream
<<<<<<< Updated upstream
=======
=======
>>>>>>> Stashed changes

            elif len(element_robot_1) > 0 and len(element_robot_2) > 0 and uid in on_livers: #botアクセス判定時にロボットフラグを付与してその時の結果を使用しない
                result = {'uid': uid, 'status': False, 'robotflag': True}
            #枠取り判定
            elif tmp_span.span.contents[0] == '今後のライブ ストリーム':
                p = parsed.find('div', class_='shelf-wrapper clearfix')
                lockup = p.find('div', class_='yt-lockup-content')

                remind_title = lockup.find('a').attrs['title']
                remind_starttime = lockup.find('span', class_='yt-badge localized-date').attrs['data-timestamp']
<<<<<<< Updated upstream
=======

                result = {'title':remind_title, 'starttime':remind_starttime}
>>>>>>> Stashed changes

                result = {'title':remind_title, 'starttime':remind_starttime}

>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
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
            
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
            element_1 = parsed.find_all('script', text=re.compile("ライブ配信中"))
            element_2 = parsed.find_all('script', text=re.compile("人が視聴中"))

            if len(element_1) > 0 and len(element_2) > 0:
                for scrp in parsed.find_all("script"):
                    if "window[\"ytInitialData\"]" in scrp.text:
                        dict_str = scrp.text.split(" = ")[1]

                        dict_str = dict_str.replace("false","False")
                        dict_str = dict_str.replace("true","True")

                        dict_str = dict_str.rstrip("  \n;")

                        dict_str = dict_str.replace('    window["ytInitialPlayerResponse"]', '')
                        dict_str = dict_str.replace(";", "")
                        
                        dics = eval(dict_str)
                        break
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

                stream_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                        ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]\
                                        ['itemSectionRenderer']['contents'][0]\
                                        ['channelFeaturedContentRenderer']['items'][0]\
                                        ['videoRenderer']

                watch = stream_description['videoId']
                title = stream_description['title']['simpleText']
                result = {'watch': watch, 'title': title, 'uid': uid, 'status': True}
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64:debug.py
=======
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
                try:
                    stream_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                            ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]\
                                            ['itemSectionRenderer']['contents'][0]\
                                            ['channelFeaturedContentRenderer']['items'][0]\
                                            ['videoRenderer']
                except KeyError:
                    result = {'uid': uid, 'status': False}

                else:
                    watch = stream_description['videoId']
                    title = stream_description['title']['simpleText']
                    result = {'watch': watch, 'title': title, 'uid': uid, 'status': True}
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
            else:
                result = {'uid': uid, 'status': False}
    return result

BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' 

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
all_liver = vlsa.get(BASE_URL)
=======
all_liver = vlsa.get(BASE_URL + 'vtuber/')
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
all_liver = vlsa.get(BASE_URL + 'vtuber/')
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
all_liver = vlsa.get(BASE_URL + 'vtuber/')
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
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
len(res)
for r in res:
    #1つ前の更新で放送中ではなかったが返ってきたステータスが放送中だった場合
    if r['status'] is not False and r['uid'] not in on_livers:
        data = {'uid': r['uid'], 'live_title': r['title'],
                'live_url': 'https://www.youtube.com/watch?v='+r['watch']}
        #on_liveに追加
        print(data)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        res = vlsa.post(BASE_URL+'onlive/', data)
=======
        res = vlsa.post(BASE_URL+'onlive', data)
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
        res = vlsa.post(BASE_URL+'onlive', data)
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
        res = vlsa.post(BASE_URL+'onlive', data)
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
    
=======
>>>>>>> Stashed changes
    #1つ前の更新で放送中で返ってきたステータスも放送中だがタイトルが変わっていた場合
    #短期間に2度続けて放送するライバーに対応するための処理
    elif r['status'] is not False and r['uid'] in on_livers:
        title = [l['live_title'] for l in on_liver if l['uid']['uid'] == r['uid']]
        if r['title'] != title[0]:
            res = vlsa.delete(BASE_URL+'onlive', r['uid'])
            data = {'uid': r['uid'], 'live_title': r['title'],
                    'live_url': 'https://www.youtube.com/watch?v='+r['watch']}
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            res = vlsa.post(BASE_URL+'onlive/', data)
    
    #1つ前の更新で放送中で返ってきたステータスが放送中ではなかった場合
    elif r['status'] is False and r['uid'] in on_livers:
        res = vlsa.delete(BASE_URL+'onlive/', r['uid'])
=======
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
            res = vlsa.post(BASE_URL+'onlive', data)

    #1つ前の更新で放送中で返ってきたステータスが放送中ではなかった場合
    elif r['status'] is False and r['uid'] in on_livers:
        res = vlsa.delete(BASE_URL+'onlive', r['uid'])
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
=======
>>>>>>> 20c8280a21be53bfe5e9e019518dd8a5eb9dbb64
