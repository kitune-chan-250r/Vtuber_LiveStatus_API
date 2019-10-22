import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os, time
import django
sys.path.append("api")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vlive_status_api.settings')
django.setup()
from api.models import *
from tqdm import tqdm

URL = 'https://vtuber-livestatus-api.herokuapp.com/api/onlive/' #heroku

logs = vlsa.get(URL)

for log in logs:
    l = LiveLog(uid=log['uid']['uid'],
                name=log['uid']['liver_name'],
                title=log['live_title'],
                gender=log['uid']['gender'],
                production=log['uid']['production'])
    l.save()
