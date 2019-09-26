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

data = [
{
    'uid': 'UCp6993wxpyDPHUpavwDFqgg',
    'liver_name': 'SoraCh. ときのそらチャンネル',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCdn5BQ06XqgXoAxIhbqw5Rg',
    'liver_name': 'フブキCh。白上フブキ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC1suqwovbL1kzsoaZgFZLKg',
    'liver_name': 'Choco Ch. 癒月ちょこ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCDqI2jOz0weumE8s7paEk6g',
    'liver_name': 'Roboco Ch. - ロボ子',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCQ0UDLQCjY0rmuxCDE38FGg',
    'liver_name': 'Matsuri Channel 夏色まつり',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC1CfXB_kRs3C-zaeTG3oGyg',
    'liver_name': 'Haato Channel 赤井はあと',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCvzGlP9oQwU--Y0r9id_jnA',
    'liver_name': 'Subaru Ch. 大空スバル',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC7fk0CB07ly8oSl0aqKkqFg',
    'liver_name': 'Nakiri Ayame Ch. 百鬼あやめ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC-hM6YJuNYVAmUWxeIr9FeA',
    'liver_name': 'Miko Ch. さくらみこ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCp-5t9SrOQwXMU7iIjQfARg',
    'liver_name': 'Mio Channel 大神ミオ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCvaTdHTWBGv3MKj3KVqJVCw',
    'liver_name': 'Okayu Ch. 猫又おかゆ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCD8HOxPs4Xvsm8H0ZxXGiBw',
    'liver_name': 'Mel Channel 夜空メルチャンネル',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCJFZiqLMntJufDCHc6bQixg',
    'liver_name': 'hololive ホロライブ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCXTpFs_3PqI41qX2d9tL2Rw',
    'liver_name': 'Shion Ch. 紫咲シオン',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UChAnqc_AY5_I3Px5dig3X1Q',
    'liver_name': 'Korone Ch. 戌神ころね',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC0TXe_LYZ4scaW2XMyi5_kw',
    'liver_name': 'AZKi Channel',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCdyqAaZDKHXg4Ahi7VENThQ',
    'liver_name': 'Noel Ch. 白銀ノエル',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCl_gCybOJRIgOXw6Qb4qJzQ',
    'liver_name': 'Rushia Ch. 潤羽るしあ',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCFTLzh12_nrtzqBPsTCqenA',
    'liver_name': 'アキロゼCh。Vtuber/ホロライブ所属',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC1DCedRgGHBdm81E1llLhOQ',
    'liver_name': 'Pekora Ch. 兎田ぺこら',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UC5CwaMl1eIgY8h02uZw7u8A',
    'liver_name': 'Suisei Channel',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCCzUftO8KOVkV4wQG1vkUvg',
    'liver_name': 'Marine Ch. 宝鐘マリン',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCvInZx9h3jC2JzsIzoOebWg',
    'liver_name': 'Flare Ch. 不知火フレア',
    'production': 'ホロライブ',
    'gender': 'woman'
},
{
    'uid': 'UCGSOfFtVCTBfmGxHK5OD8ag',
    'liver_name': 'Ankimo Ch. あん肝チャンネル',
    'production': 'ホロライブ',
    'gender': 'woman'
}]

URL = 'http://localhost:8000/api/'

for d in data:
    err = vlsa.post(URL, d)



