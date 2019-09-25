import Vtuber_LiveStatus_API_lib as vlsa

BASE_URL = 'http://localhost:8000/api/'

data = {'uid':'UCsumple', 'live_title':'testpost'}

res = vlsa.delete(BASE_URL + 'onlive', 'UCsumple')
print(res)