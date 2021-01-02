import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re, requests, datetime
import Vtuber_LiveStatus_API_lib as vlsa

'''
def gethtml(uid):
    aiphttpでhtmlデータ収集
    return htmlデータ

def parshtml(html):
    bs4でパースして必要なデータ収集
    return result{onlive:{}, reminder:{}}

APIから全てのvtuberのuidを取得

requestで放送中のデータをAPIから取得、uidをリスト化

gethtmlメソッドを非同期で実行->結果をリスト化[{uid:html}]

gethtmlメソッドの結果を非同期で実行したparshtmlに渡す

apiのreminderデータを取得

reminder 全件削除

非同期で取得したonlive内のデータから新規の放送はapiへpost、終わった放送はdelete、reminderは全件post

'''

async def getHtml_aiohttp(uid):
    #url = 'https://vtuber-livestatus-api.herokuapp.com/api/onlive'
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    async with aiohttp.ClientSession(headers=hed) as session:
            async with session.get(url) as response:
                return { 'uid': uid, 'html': await response.text()}

async def parsHtml(uidhtml):
    parsed = BeautifulSoup(uidhtml['html'], "html.parser")
    yuid = uidhtml['uid']
    dics = {}
            
    #element_1 = parsed.find_all('script', text=re.compile("ライブ配信中"))len(element_1) > 0 and 
    element_2 = parsed.find_all('script', text=re.compile("人が視聴中"))
    remind = parsed.find_all('script', text=re.compile("今後のライブ ストリーム"))
    
    result = {}
    result['onlive'] = {'uid': yuid, 'status': False}

    if len(element_2) or len(remind) > 0:
        pattern = re.compile(r"var ytInitialData = .") 
        ytinitialdata = parsed.find("script",text=pattern)

        dict_str = str(ytinitialdata).split(" = ")[1]

        dict_str = dict_str.replace("false","False")
        dict_str = dict_str.replace("true","True")

        dict_str = dict_str.rstrip("  \n;")

        dict_str = dict_str.replace('    window["ytInitialPlayerResponse"]', '')
        dict_str = dict_str.replace(';', '')
        dict_str = dict_str.replace('</script>', '')
        dics = eval(dict_str)

    if len(element_2) > 0:
        try:
            stream_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                    ["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]\
                                    ['itemSectionRenderer']['contents'][0]\
                                    ['channelFeaturedContentRenderer']['items'][0]['videoRenderer']
        except KeyError:
            result['onlive'] = {'uid': yuid, 'status': False}
        else:
            watch = stream_description['videoId']
            
            try:
                title = stream_description['title']['runs'][0]['text']
            except KeyError:
                title = "データ取得失敗 KeyError: stream_description['title']['simpleText']"

            result['onlive'] = {'watch': watch, 'title': title, 'uid': yuid, 'status': True, 'flag': 'onlive'}

    elif len(remind) > 0:
        reminder_description = dics["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0]\
                                   ["tabRenderer"]["content"]["sectionListRenderer"]["contents"]
        is_not_grid = True
        
        for rem in reminder_description:
            if '今後のライブ ストリーム' in str(rem):
                try:
                    contents = rem['itemSectionRenderer']['contents'][0]\
                                ['shelfRenderer']["content"]['expandedShelfContentsRenderer']['items']
                except KeyError:
                    contents = rem['itemSectionRenderer']['contents'][0]\
                              ['shelfRenderer']["content"]['horizontalListRenderer']['items']
                    is_not_grid = False
                
                for reminds in contents:
                    if is_not_grid:
                        reminds = reminds['videoRenderer']
                    else:
                        reminds = reminds['gridVideoRenderer']
                    reminder_watch = reminds['videoId']
                    reminder_title = reminds['title']['simpleText']
                    try:
                        reminder_date = reminds['upcomingEventData']['startTime'] #UNIX time
                    except KeyError:
                        reminder_data = 0
                        print(reminds)
                    try:
                        audience = reminds['shortViewCountText']['runs'][0]['text']
                    except KeyError:
                        audience = 0
                    result['reminder'] = {'watch': reminder_watch, 'title': reminder_title, 'uid': yuid,'start_datetime': reminder_date, 'audience': audience, 'flag': 'reminder'}

                    break
    else:
        result['onlive'] = {'uid': yuid, 'status': False, 'flag': 'onlive'}

    return result

uids = ['UCspv01oxUFf_MTSipURRhkA', 'UC9V3Y3_uzU5e-usObb6IE1w']
BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' 

all_liver = vlsa.get(BASE_URL + 'vtuber/')
on_liver = vlsa.get(BASE_URL + 'onlive/')

if len(on_liver) != 0:
    on_livers = [liver['uid']['uid'] for liver in on_liver]
else:
    on_livers = []

uids = [liver['uid'] for liver in all_liver]

#getHtml activate
loop = asyncio.get_event_loop()
done, pending = loop.run_until_complete(asyncio.wait([getHtml_aiohttp(uid) for uid in uids]))
#res = [d.result() for d in done] #結果
uidhtmlList = [h.result() for h in done]

#parsHtml activate
done, pending = loop.run_until_complete(asyncio.wait([parsHtml(text) for text in uidhtmlList]))
dataList = [w.result() for w in done]
print(dataList, len(dataList))

reminder = vlsa.get(BASE_URL + 'reminder')
#reminder all reset
for remind in reminder:
    res_reminder = vlsa.delete(BASE_URL+'reminder', remind['uid'])

async def dataReload(livedata):
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
