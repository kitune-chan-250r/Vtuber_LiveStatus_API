import requests, json, os

TOKEN = os.environ['TOKEN']


#auth
headers={'Authorization': 'Token {}'.format(TOKEN)}

#get request, return=json data
def get(URL):
   return requests.get(URL).json()

#post request with dict data, return=status
def post(URL, data):
	return requests.post(URL, data, headers=headers)

#delete request with uid, return=status
def delete(URL, uid):
	return requests.delete(URL +'/{0}/'.format(str(uid)), headers=headers)

#get request with query, return=json data
def get_with_q(URL, pk):
    return requests.get(URL + 'onlive/?pr={0}'.format(pk)).json()

