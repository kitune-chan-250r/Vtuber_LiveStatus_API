import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os, time
import django
sys.path.append("api")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vlive_status_api.settings')
django.setup()
from api.models import *
from tqdm import tqdm
import threading

#BASE_URL = 'http://localhost:8000/api/' #local
BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' #heroku

#channel idを受け取って放送中の場合は配信場所のURL、そうでない場合はFalseを返す
def live_status(channelid):
    youtube_url = "https://www.youtube.com"
    channel_site_url = youtube_url + "/channel/"
    channel_site_url += channelid
    hed = {'Accept-Language': 'ja'}
    html_data = requests.get(channel_site_url, headers=hed)
    parsed = bs4.BeautifulSoup(html_data.content, "html.parser")

    element_1 = parsed.find_all("li", text=re.compile("ライブ配信中"))
    element_2 = parsed.find_all("li", text=re.compile("人が視聴中"))

    if len(element_1) > 0 and len(element_2) > 0:
        watch = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").attrs['href']
        title = parsed.find("a", class_="yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2").text
        return {'watch': watch.replace('/watch?v=', ''), 'title': title}
    else:
        return False

all_liver = vlsa.get(BASE_URL)
on_liver = vlsa.get(BASE_URL + 'onlive/')

uids = [liver['uid'] for liver in all_liver]
if len(on_liver) != 0:
    on_livers = [liver['uid']['uid'] for liver in on_liver]
else:
    on_livers = []

div = len(all_liver) // 2

ll1 = uids[:div]
ll2 = uids[div:]

def reqtask(uids):
    for uid in uids:
        status = live_status(uid)
        print(status, uid)
        if status is not False and uid not in on_livers:
            data = {'uid': uid, 'live_title': status['title'],
                 'live_url': 'https://www.youtube.com/watch?v='+status['watch']}
            #on_liveに追加
            res = vlsa.post(BASE_URL+'onlive', data)

        elif status is not False and uid in on_livers:
            title = [l['live_title'] for l in on_liver if l['uid']['uid'] == uid]
            print(title, status['title'])
            if status['title'] != title[0]:
                res = vlsa.delete(BASE_URL+'onlive', uid)
                data = {'uid': uid, 'live_title': status['title'],
                 'live_url': 'https://www.youtube.com/watch?v='+status['watch']}
                res = vlsa.post(BASE_URL+'onlive', data)

        elif status is False and uid in on_livers:
            #on_liveから外す
            res = vlsa.delete(BASE_URL+'onlive', uid)


th1 = threading.Thread(target=reqtask, args=(ll1,))
th2 = threading.Thread(target=reqtask, args=(ll2,))

th1.start()
th2.start()