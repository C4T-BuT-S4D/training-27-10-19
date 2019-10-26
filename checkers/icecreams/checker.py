#!/usr/bin/env python3

import sys
import requests
import checklib
from ice_lib import CheckMachine


def check_html_page(page):
    checklib.assert_in('/register.html', page, 'No register link')
    checklib.assert_in('/login.html', page, 'No login link')
    checklib.assert_in('/add.html', page, 'No add link')
    checklib.assert_in('/icecreams', page, 'No icecreams link')
    checklib.assert_in('/lastusers', page, 'No lastusers link')


def put(host, flag_id, flag, vuln):
    cm = CheckMachine(host)

    register_resp = cm.get_register_page()
    checklib.assert_in('registerForm', register_resp, 'No registration form')
    check_html_page(register_resp)
    password = None
    if vuln == '2':
        password = flag
    login, password = cm.register_service(password=password)

    login_resp = cm.get_login_page()
    check_html_page(login_resp)
    checklib.assert_in('loginForm', login_resp, 'No login form')
    sess = cm.login_in_service(login, password)

    resp = cm.get_add_page(sess)
    check_html_page(resp)
    checklib.assert_in('addForm', resp, 'No add form')
    icecream_name = checklib.rnd_string(20)
    if vuln == '1':
        icecream_name = flag
    resp = cm.add_icecream(sess, icecream_name)
    checklib.assert_in('Icecream added', resp, 'Failed to add icecream')
    checklib.cquit(checklib.Status.OK, f'{login}:{password}:{icecream_name}')

def get(host, flag_id, flag, vuln):
    cm = CheckMachine(host)
    login, password, icecream_name = flag_id.split(':')
    login_resp = cm.get_login_page()
    check_html_page(login_resp)
    checklib.assert_in('loginForm', login_resp, 'No login form')
    sess = cm.login_in_service(login, password)
    my_icecreams = cm.get_my_icecreams(sess)
    checklib.assert_in(icecream_name, my_icecreams, 'Failed to get user icecreams', status=checklib.Status.CORRUPT)
    checklib.cquit(checklib.Status.OK)


def check(host):
    cm = CheckMachine(host)

    index_resp = cm.get_index()
    check_html_page(index_resp)

    register_resp = cm.get_register_page()
    checklib.assert_in('registerForm', register_resp, 'No registration form')
    check_html_page(register_resp)
    login, password = cm.register_service()

    login_resp = cm.get_login_page()
    check_html_page(login_resp)
    checklib.assert_in('loginForm', login_resp, 'No login form')
    sess = cm.login_in_service(login, password)

    resp = cm.get_add_page(sess)
    check_html_page(resp)
    checklib.assert_in('addForm', resp, 'No add form')
    icecream_name = checklib.rnd_string(20)
    resp = cm.add_icecream(sess, icecream_name)
    checklib.assert_in('Icecream added', resp, 'Failed to add icecream')
    my_icecreams = cm.get_my_icecreams(sess)
    checklib.assert_in(icecream_name, my_icecreams, 'Failed to get user icecreams')
    checklib.cquit(checklib.Status.OK)


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
            checklib.cquit(checklib.Status.ERROR, 'System error', 'Unknown action: ' + action)

    except requests.exceptions.ConnectionError:
        checklib.cquit(checklib.Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        checklib.cquit(checklib.Status.ERROR, 'System error', str(e))
