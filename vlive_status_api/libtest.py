import Vtuber_LiveStatus_API_lib as vlsa

BASE_URL = 'http://localhost:8000/api/'

res = vlsa.get(BASE_URL)
print(res)