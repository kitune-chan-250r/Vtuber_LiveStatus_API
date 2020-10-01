import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import requests

def get(URL):
   return requests.get(URL).json()



async def main(uid):
    hed = {'Accept-Language': 'ja'}
    url = "https://www.youtube.com/channel/" + uid
    async with aiohttp.ClientSession(headers=hed) as session:
        async with session.get(url) as response:
            html = await response.text()
            parsed = BeautifulSoup(html, "html.parser")
            
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
                    print(title)
                    result = {'watch': watch, 'title': title, 'uid': uid, 'status': True}
            else:
                result = {'uid': uid, 'status': False}
    return result

BASE_URL = 'https://vtuber-livestatus-api.herokuapp.com/api/' 

all_liver = get(BASE_URL + 'vtuber/')
on_liver = get(BASE_URL + 'onlive/')
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

