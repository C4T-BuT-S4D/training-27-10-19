#!/usr/bin/env python3

import re
import sys
import json
import requests

from random import choice, getrandbits
from string import ascii_lowercase, digits
from checklib import cquit, Status

from sss import recover_secret


PORT = 17171

VULN_SSS = '1'
VULN_PROVE = '2'

PRIME = 12058950698856173324983236458418086340362644737326952033848207975666636738909947835100603153200557571796444486564391552670171783376177474858071463819335779


def random_int(bits=512):
    return getrandbits(bits)


def random_str(length=20):
    alpha = ascii_lowercase + digits
    return ''.join(choice(alpha) for _ in range(length))


def add_pack(url, name, flavour):
    data = {
        'name': name,
        'flavour': flavour
    }
    try:
        response = requests.post(url + '/addPack', json=data).json()
    except Exception:
        cquit(Status.MUMBLE, 'Invalid JSON response')
    if not response.get('success', False):
        cquit(Status.MUMBLE, 'Can not add a new pack')
    if 'guid' not in response:
        cquit(Status.MUMBLE, 'Can not get guid of new pack')
    if 'sugar' not in response:
        cquit(Status.MUMBLE, 'Can not get sugar of new pack')
    guid, sugar = response['guid'], response['sugar']
    try:
        sugar = int(sugar)
    except Exception:
        cquit(Status.MUMBLE, 'Sugar must be int')
    return guid, sugar


def add_marshmallow(url, sugar, filling, is_private):
    data = {
        'sugar': sugar,
        'filling': filling,
        'isPrivate': is_private
    }
    try:
        response = requests.post(url + '/addMarshmallow', json=data).json()
    except Exception:
        cquit(Status.MUMBLE, 'Invalid JSON response')
    if not response.get('success', False):
        cquit(Status.MUMBLE, 'Can not add a new marshmallow')
    if 'guid' not in response:
        cquit(Status.MUMBLE, 'Can not get guid of new marshmallow')
    guid = response['guid']
    return guid


def get_pack(url, guid):
    html = requests.get(url + '/packs/' + guid).text
    if 'Pack not found' in html:
        cquit(Status.MUMBLE, 'Can not find a pack')
    values = re.findall('value="(.*?)"', html)
    if len(values) < 3:
        cquit(Status.MUMBLE, 'Pack fields do not exist')
    guid_val, name_val, flavour_val = values[:3]
    if guid != guid_val:
        cquit(Status.MUMBLE, 'Guids should be the same')
    marshmallows = re.findall('href="/marshmallows/(.*?)"', html)
    if len(marshmallows) == 0:
        cquit(Status.MUMBLE, 'Can not find marshmallows in the pack')
    return name_val, flavour_val, marshmallows


def get_marshmallow(url, guid):
    html = requests.get(url + '/marshmallows/' + guid).text
    if 'Marshmallow not found' in html:
        cquit(Status.MUMBLE, 'Can not find a marshmallow')
    values = re.findall('value="(.*?)"', html)
    if len(values) < 2:
        cquit(Status.MUMBLE, 'Marshmallow fields do not exist')
    guid_val, sugar_val = values[:2]
    if guid != guid_val:
        cquit(Status.MUMBLE, 'Guids should be the same')
    try:
        sugar = int(sugar_val)
    except Exception:
        cquit(Status.MUMBLE, 'Sugar must be int')
    is_private = 'Marshmallow is private' in html
    if not is_private:
        filling_val = values[2]
    else:
        filling_val = None
    return sugar, is_private, filling_val


def prove_marshmallow(url, guid, filling):
    data = {
        'filling': filling
    }
    try:
        response = requests.post(url + '/marshmallows/' + guid, json=data).json()
    except Exception:
        cquit(Status.MUMBLE, 'Invalid JSON response')
    if not response.get('success', False):
        cquit(Status.MUMBLE, 'Can not prove a marshmallow')
    if 'filling' not in response:
        cquit(Status.MUMBLE, 'Can not find filling in prove response')
    return response['success'], response['filling']


def list_all_marshmallows(url):
    try:
        html = requests.get(url + '/marshmallows').text
    except Exception:
        cquit(Status.MUMBLE, 'Can not get marshmallows list')
    return re.findall('"/marshmallows/(.*?)"', html)


def list_all_packs(url):
    try:
        html = requests.get(url + '/packs').text
    except Exception:
        cquit(Status.MUMBLE, 'Can not get packs list')
    return re.findall('"/packs/(.*?)"', html)


def extract_secret(url, sugar, marshmallows):
    shares = [(1, sugar)]
    for marshmallow in marshmallows:
        sugar_, is_private, filling = get_marshmallow(url, marshmallow)
        shares.append((len(shares) + 1, sugar_))
    try:
        number = recover_secret(shares, PRIME)
    except Exception:
        cquit(Status.MUMBLE, 'Incorrect sugar values')
    return number.to_bytes(64, 'little').replace(b'\x00', b'')


def put(host, flag_id, flag, vuln):
    url = 'http://%s:%d' % (host, PORT)

    if vuln == VULN_SSS:
        guid, sugar = add_pack(url, random_str(), flag)
        flag_id = {'guid': guid, 'sugar': sugar}
        cquit(Status.OK, json.dumps(flag_id))

    if vuln == VULN_PROVE:
        guid = add_marshmallow(url, random_int(), flag, True)
        flag_id = {'guid': guid}
        cquit(Status.OK, json.dumps(flag_id))

    cquit(Status.ERROR, 'Unknown vuln')


def get(host, flag_id, flag, vuln):
    url = 'http://%s:%d' % (host, PORT)

    if vuln == VULN_SSS:
        flag_id = json.loads(flag_id)
        guid, sugar = flag_id['guid'], flag_id['sugar']
        name, flavour, marshmallows = get_pack(url, guid)
        actual_flag = extract_secret(url, sugar, marshmallows)
        if flag.encode() in actual_flag or actual_flag in flag.encode():
            cquit(Status.OK)
        else:
            cquit(Status.CORRUPT, 'Can not get flag from packs')

    if vuln == VULN_PROVE:
        flag_id = json.loads(flag_id)
        guid = flag_id['guid']
        success, filling = prove_marshmallow(url, guid, flag)
        if filling in flag or flag in filling:
            cquit(Status.OK)
        else:
            cquit(Status.CORRUPT, 'Can not get flag from marshmallows')

    cquit(Status.ERROR, 'Unknown vuln')


def check(host):
    url = 'http://%s:%d' % (host, PORT)

    def check_marshmallow(is_private):
        sugar, filling = random_int(), random_str()
        guid = add_marshmallow(url, sugar, filling, is_private)

        if guid not in list_all_marshmallows(url):
            cquit(Status.MUMBLE, 'Can not find marshmallow in list')

        sugar_, is_private_, filling_ = get_marshmallow(url, guid)
        if sugar != sugar_:
            cquit(Status.MUMBLE, 'Sugars are not the same')
        if is_private != is_private_:
            cquit(Status.MUMBLE, 'Private status is not the same')
        
        success, filling_ = prove_marshmallow(url, guid, filling)
        if not success or filling != filling_:
            cquit(Status.MUMBLE, 'Fillings are not the same')

    def check_pack():
        name, flavour = random_str(), random_str()
        guid, sugar = add_pack(url, name, flavour)

        if guid not in list_all_packs(url):
            cquit(Status.MUMBLE, 'Can not find pack in list')

        name_, flavour_, marshmallows = get_pack(url, guid)
        if name != name_:
            cquit(Status.MUMBLE, 'Names are not the same')
        
        flavour_ = extract_secret(url, sugar, marshmallows)
        if flavour.encode() not in flavour_ or flavour_ not in flavour.encode():
            cquit(Status.MUMBLE, 'Flavours are not the same')

    check_marshmallow(True)
    check_marshmallow(False)

    check_pack()
    cquit(Status.OK)


if __name__ == '__main__':
    action, *args = sys.argv[1:]

    try:
        if action == "check":
            host, = args
            check(host)
        elif action == "put":
            host, flag_id, flag, vuln = args
            put(host, flag_id, flag, vuln)
        elif action == "get":
            host, flag_id, flag, vuln = args
            get(host, flag_id, flag, vuln)
        else:
            cquit(Status.ERROR, 'System error', 'Unknown action: ' + action)

        cquit(Status.ERROR, 'System error', f'Action {action} did not cquit')
        
    except requests.exceptions.ConnectionError:
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))
