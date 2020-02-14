import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import Vtuber_LiveStatus_API_lib as vlsa
from tqdm import tqdm

parsed = ''

async def main(uid):
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
        res = vlsa.delete(BASE_URL+'onlive', r['uid'])

#連続してdeleteに入った場合
on_liver = vlsa.get(BASE_URL + 'onlive/')
if len(on_liver) != 0:
    livers = [liver['uid']['uid'] for liver in on_liver]
else:
    livers = []

if len(on_livers) != 0 and len(livers) == 0:
    print('[EORROR] : all_delete ', parsed)