from hashlib import sha512
from checklib import *
from time import sleep
import secrets
import requests
import json

PORT = 9999

def hchecksum(text):
    h = text.encode()
    for i in range(1000):
        h = sha512(h).hexdigest().encode()
    sleep(1)
    return h.decode()

class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}/api'
    

    def __init__(self, host, port):
        self.host = host
        self.port = port


    def gen_kozi(self):
        kozi = {
            'name': rnd_string(8),
            'fortune': rnd_string(15),
        }
        return kozi


    def register_in_service(self):
        register_url = f'{self.url}/register/'
        login = rnd_username()
        password = rnd_password()
        data = {
            'username': login,
            'password': password
        }
        r = requests.post(url=register_url, json=data)
        try:
            assert_eq(r.json(), {'result': 'ok'}, "Can't register in service")
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on register')
        return data


    def login_in_service(self, login, password):
        login_url = f'{self.url}/login/'
        session = requests.Session()
        login_data = {
            'username': login,
            'password': password
        }
        r = session.post(url=login_url, json=login_data)
        try:
            assert_eq(r.json(), {'result': 'ok'}, "Can't login in service")
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on login')
        return session


    def create_kozinak(self, session, kozi):
        chk = hchecksum(kozi['fortune'])
        create_url = f'{self.url}/kozi/'
        create_data = {
            'name': kozi['name'],
            'fortune': kozi['fortune'],
            'checksum': chk,
            'pipe': kozi.get('pipe')
        }

        r = session.post(url=create_url, json=create_data)
        try:
            assert_eq(r.json(), {'result': 'ok'}, "Can't login in service")
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on kozinak create')


    def list_kozinak(self):
        list_url = f'{self.url}/list/'

        r = requests.get(url=list_url)
        try:
            assert_in("result", r.json(), 'Invalid json on kozinak list')
            assert_eq(type(r.json()["result"]), type([]), 'Invalid json on kozinak list')
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on kozinak list')
        return r.json()["result"]


    def get_kozinak(self, session, fullname):
        get_url = f'{self.url}/kozi/{fullname}/'

        r = session.get(url=get_url)
        try:
            assert_in("result", r.json(), 'Invalid json on kozinak get')
            assert_eq(type(r.json()["result"]), type({}), 'Invalid json on kozinak get')
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on kozinak get')
        return r.json()["result"]


    def open_kozinak(self, session, fullname):
        open_url = f'{self.url}/open_kozi/'
        open_data = {
            'kozi': fullname
        }

        r = session.post(url=open_url, json=open_data)
        try:
            assert_eq(r.json(), {'result': 'ok'}, "Can't open kozinak")
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on kozinak open')


    def copy_kozinak(self, session, name, url):
        copy_url = f'{self.url}/copy_kozi/'
        copy_data = {
            'name': name,
            'url': url,
        }

        r = session.post(url=copy_url, json=copy_data)
        try:
            assert_eq(r.json(), {'result': 'ok'}, "Can't copy kozinak")
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on kozinak copy')


    def exec_kozinak(self, session, fullname):
        exec_url = f'{self.url}/exec_kozi/{fullname}/'

        r = session.get(url=exec_url)
        try:
            assert_in("result", r.json(), 'Invalid json on kozinak exec')
            assert_eq(type(r.json()["result"]), type(""), 'Invalid json on kozinak exec')
        except json.decoder.JSONDecodeError:
            cquit(Status.MUMBLE, 'Invalid json on kozinak exec')
        return r.json()["result"]
