import requests, json

#get request, return=json data
def get(URL):
   return requests.get(URL).json()

#post request with json data, return=status
def post(URL, data):
    pass

#delete request with uid, return=status
def delete(URL, uid):
    pass

#get request with query, return=json data
def get_with_q(URL, pk):
    pass