import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os, time
import django
sys.path.append("api")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vlive_status_api.settings')
django.setup()
from api.models import *
from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


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
