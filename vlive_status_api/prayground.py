import Vtuber_LiveStatus_API_lib as vlsa
import requests, bs4, re, sys, os
import django
sys.path.append("api")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vlive_status_api.settings')
django.setup()
from api.models import *


print(On_Live.objects.all().delete())