import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os, time
import django
sys.path.append("api")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vlive_status_api.settings')
django.setup()
from api.models import *
from tqdm import tqdm


'''
url = "https://virtual-youtuber.userlocal.jp/office/cover" 
html_data = requests.get(url)
parsed = bs4.BeautifulSoup(html_data.content, "html.parser")


lis = parsed.find_all('span', class_='text-secondary')
chname = [i.string for i in lis]
print(chname)

"""
propagation = parsed.find_all('a', class_='no-propagation')1
for s in propagation:
    print(s.attrs['href'])
"""

source = 'https://www.youtube.com/results?search_query='#'https://virtual-youtuber.userlocal.jp/'

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

result = []

for c in tqdm(chname):
    driver.get(source + c)
    time.sleep(3)
    p = bs4.BeautifulSoup(driver.page_source, "html.parser")
    try:
        ch = p.find('a', class_='yt-simple-endpoint style-scope ytd-channel-renderer').attrs['href']
    except AttributeError:
        ch = "none"

    ch = ch.replace('/channel/', '')
    data = {'uid': ch,
            'liver_name': c,
            'production': 'ホロライブ',
            'gender': 'woman'}
    result.append(data)

print(result)
'''

'''BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' #heroku
all_liver = vlsa.get(BASE_URL)
on_liver = vlsa.get(BASE_URL + 'onlive/')

uids = [liver['uid'] for liver in all_liver]
if len(on_liver) != 0:
    on_livers = [liver['uid']['uid'] for liver in on_liver]
else:
    on_livers = []


def live_status(channelid):
    youtube_url = "https://www.youtube.com"
    channel_site_url = youtube_url + "/channel/"
    channel_site_url += channelid
    html_data = requests.get(channel_site_url)
    parsed = bs4.BeautifulSoup(html_data.content, "html.parser")

    print(parsed)

    element_1 = parsed.find_all("li", text=re.compile("ライブ配信中"))
    element_2 = parsed.find_all("li", text=re.compile("人が視聴中"))

    if len(element_1) > 0 and len(element_2) > 0:
        watch = parsed.find("a", class_="yt-uix-sessionlink", href=re.compile("/watch"))
        live = watch.get("href") #str(ref.lstrip("/watch?v="))
        return youtube_url + live
    else:
        return False

live_status("UC-hM6YJuNYVAmUWxeIr9FeA")
'''

youtube_url = "https://www.youtube.com"
channel_site_url = youtube_url + "/channel/UC-hM6YJuNYVAmUWxeIr9FeA"
hed = {'Accept-Language': 'ja'}
html_data = requests.get(channel_site_url, headers=hed)
parsed = bs4.BeautifulSoup(html_data.content, "html.parser")

print(parsed.find('html').attrs['lang'])