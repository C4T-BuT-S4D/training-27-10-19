#!/usr/bin/env python3

import os
import sys
import enum
import string
import requests
import secrets
import random

from checklib import *
from choco_lib import *


def put(host, flag_id, flag, vuln):
    mch = CheckMachine(host)
    username, password = mch.register_user()
    sess = mch.login_user(username, password)

    name = rnd_string(20)
    description = rnd_string(random.randint(100, 200)) + flag + rnd_string(random.randint(100, 200))
    mch.add_chocolate(sess, name, description)
    ids, names = mch.get_my_chocolates(sess)

    wrappers = []
    for i in range(5):
        wrap_name = rnd_string(20)
        wrappers.append(wrap_name)
        mch.add_wrapper(sess, wrap_name)

    cquit(Status.OK, f'{ids[-1]}:{username}:{password}:{",".join(wrappers)}')


def get(host, flag_id, flag, vuln):
    mch = CheckMachine(host)
    choco_id, username, password, wrappers = flag_id.split(':')
    sess = mch.login_user(username, password)
    choco_page = mch.get_chocolate(sess, choco_id)
    assert_in(flag, choco_page, 'Could not get flag from service', status=Status.CORRUPT)

    wrappers = wrappers.split(',')
    random.shuffle(wrappers)
    cnt = len(wrappers) // 2 + 1
    guesses = ','.join(wrappers[:cnt])

    user2, pass2 = mch.register_user()
    sess = mch.login_user(user2, pass2)
    ids, names = mch.get_users(sess)
    assert_in(username, names, "Could not find registered user")

    user_id = ids[names.index(username)]

    mch.make_friends(sess, user_id, guesses)
    choco_page = mch.get_chocolate(sess, choco_id)
    assert_in(flag, choco_page, 'Could not get flag from service', status=Status.CORRUPT)    

    cquit(Status.OK)


def check(host):
    mch = CheckMachine(host)
    index_page = mch.get_index(requests)
    assert_in('/User/Login', index_page, 'No login link')
    assert_in('/User/Register', index_page, 'No register link')
    assert_in('/User/List', index_page, 'No users list link')

    username, password = mch.register_user()
    sess = mch.login_user(username, password)
    index_page = mch.get_index(sess)
    assert_in(username, index_page, 'No Me link')
    assert_in('/User/Me', index_page, 'No Me link')

    ids, names = mch.get_users(sess)
    assert_in(username, names, "Could not find registered user")

    user_id = ids[names.index(username)]

    me_page = mch.get_me(sess)
    assert_in(username, me_page, 'No username on Me')

    choco_name = rnd_string(20)
    description = rnd_string(50)
    mch.add_chocolate(sess, choco_name, description)

    wrap_count = random.randint(5, 10)
    wrappers = []
    for _ in range(wrap_count):
        name = rnd_string(20)
        mch.add_wrapper(sess, name)
        wrappers.append(name)

    ids, names = mch.get_my_chocolates(sess)
    assert_in(choco_name, names, 'Could not find chocolate name in list')

    choco_id = ids[names.index(choco_name)]

    ids, names = mch.get_my_wrappers(sess)
    for wrapper in wrappers:
        assert_in(wrapper, names, 'Could not find wrapper name in list')

    to_check = random.choice(range(len(wrappers)))
    wrapper_id = ids[names.index(wrappers[to_check])]
    wrapper_page = mch.get_wrapper(sess, wrapper_id)
    assert_in(wrappers[to_check], wrapper_page, 'Could not find chocolate name in view')

    ids, names = mch.get_user_chocolates(requests, user_id)
    assert_in(choco_name, names, 'Could not find chocolate name in list')

    user2, pass2 = mch.register_user()
    sess = mch.login_user(user2, pass2)

    cnt_to_guess = min(len(wrappers) // 2 + random.randint(1, 3), len(wrappers))
    random.shuffle(wrappers)
    guesses = ','.join(wrappers[:cnt_to_guess])

    mch.make_friends(sess, user_id, guesses)
    choco_page = mch.get_chocolate(sess, choco_id)
    assert_in(description, choco_page, 'Could not get friend\'s chocolate')    

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

        cquit(Status.ERROR)
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        raise
        cquit(Status.ERROR, 'System error', str(e))
