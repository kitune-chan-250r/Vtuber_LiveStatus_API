import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os
import django
sys.path.append("api")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vlive_status_api.settings')
django.setup()
from api.models import *

BASE_URL = 'http://localhost:8000/api/'

#channel idを受け取って放送中の場合は配信場所のURL、そうでない場合はFalseを返す
def live_status(channelid):
    youtube_url = "https://www.youtube.com"
    channel_site_url = youtube_url + "/channel/"
    channel_site_url += channelid
    html_data = requests.get(channel_site_url)
    parsed = bs4.BeautifulSoup(html_data.content, "html.parser")

    element_1 = parsed.find_all("li", text=re.compile("ライブ配信中"))
    element_2 = parsed.find_all("li", text=re.compile("人が視聴中"))

    if len(element_1) > 0 and len(element_2) > 0:
        watch = parsed.find("a", class_="yt-uix-sessionlink", href=re.compile("/watch"))
        live = watch.get("href") #str(ref.lstrip("/watch?v="))
        return youtube_url + live
    else:
        return False

def get_live_title(live_url):
    html_data = requests.get(live_url)
    parsed = bs4.BeautifulSoup(html_data.content, "html.parser")
    return parsed.find('span', class_='watch-title metadata-updateable-title').text


all_liver = Vtuber.objects.all()
on_liver = On_Live.objects.all()

uids = [liver.uid for liver in all_liver]
if len(on_liver) != 0:
    on_livers = [liver.uid.uid for liver in on_liver]

for uid in uids:
    status = live_status(uid)
    if status is not False and uid not in on_livers:
        title = get_live_title(status)
        data = {'uid': uid, 'live_title': title, 'live_url': status}
        #on_liveに追加
        res = vlsa.post(BASE_URL+'onlive', data)
    elif uid in on_livers:
        #on_liveから外す
        res = vlsa.delete(BASE_URL+'onlive', uid)
