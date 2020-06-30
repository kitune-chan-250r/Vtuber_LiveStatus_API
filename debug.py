import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import requests
import requests_html as rh
import Vtuber_LiveStatus_API_lib as vlsa

BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/'

async def main(uid):
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    asysession = rh.AsyncHTMLSession()

    asysession.headers.update(hed)
    r = await asysession.get(url)
    await r.html.arender()

    element = r.html.find("span.ytd-shelf-renderer")[0].text
    if element == 'ライブ配信中':
        livedetail = r.html.find('a.yt-simple-endpoint.style-scope.ytd-video-renderer')[0].attrs
        result = {'watch': livedetail['href'].replace('/watch?v=', ''), 'title': livedetail['title'], 'uid': uid, 'status': True}
    else:
        result = {'uid': uid, 'status': False}


    return result

#uids = ["UCSFCh5NL4qXrAy9u-u2lX3g", "UCqm3BQLlJfvkTsX_hvm0UmA"]

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

res = [d.result() for d in done]

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


'''session = rh.HTMLSession()
r = session.get('https://www.youtube.com/channel/UCSFCh5NL4qXrAy9u-u2lX3g')
r.html.render()
element = r.html.find('a.yt-simple-endpoint.style-scope.ytd-video-renderer')[0].attrs

print(element)'''