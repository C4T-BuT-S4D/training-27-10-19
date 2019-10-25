#!/usr/bin/env python3

from kozi_lib import *
import sys
import requests

def put(host, flag_id, flag, vuln):
    mch = CheckMachine(host, PORT)

    data = mch.register_in_service()
    s = mch.login_in_service(data['username'], data['password'])

    flag_part1 = flag[:15]
    flag_part2 = flag[15:]

    kozi1 = mch.gen_kozi()
    kozi2 = mch.gen_kozi()

    kozi2['fortune'] = flag_part2
    kozi1['fortune'] = flag_part1
    kozi1['pipe'] = f"{data['username']}_{kozi2['name']}"

    mch.create_kozinak(s, kozi1)
    mch.create_kozinak(s, kozi2)

    cquit(Status.OK, f"{data['username']}:{data['password']}:{kozi1['name']}")


def get(host, flag_id, flag, vuln):
    mch = CheckMachine(host, PORT)
    username, password, kozi_name = flag_id.split(':')

    s = mch.login_in_service(username, password)
    
    exec_result = mch.exec_kozinak(s, f"{username}_{kozi_name}")

    assert_eq(flag, exec_result, 'Invalid flag in kozinak exec')

    cquit(Status.OK)

def check(host):
    mch = CheckMachine(host, PORT)

    data = mch.register_in_service()
    s = mch.login_in_service(data['username'], data['password'])

    kozi1 = mch.gen_kozi()

    mch.create_kozinak(s, kozi1)

    l = mch.list_kozinak()
    assert_in(f"{data['username']}_{kozi1['name']}", l, "Can't add kozinak")

    k = mch.get_kozinak(s, f"{data['username']}_{kozi1['name']}")

    assert_in('name', k, 'Invalid json on kozinak get')
    assert_eq(k['name'], kozi1['name'], 'Invalid kozinak on kozinak get')
    assert_in('fortune', k, 'Invalid json on kozinak get')
    assert_eq(k['fortune'], kozi1['fortune'], 'Invalid kozinak on kozinak get')
    assert_in('owner', k, 'Invalid json on kozinak get')
    assert_eq(k['owner'], data['username'], 'Invalid kozinak on kozinak get')
    if kozi1.get('pipe') is not None:
        assert_in('pipe', k, 'Invalid json on kozinak get')
        assert_eq(k['pipe'], kozi1['pipe'], 'Invalid kozinak on kozinak get')

    mch.open_kozinak(s, f"{data['username']}_{kozi1['name']}")

    s_nobody = requests.Session()

    k = mch.get_kozinak(s_nobody, f"open_{kozi1['name']}")

    assert_in('name', k, 'Invalid json on kozinak get')
    assert_eq(k['name'], kozi1['name'], 'Invalid kozinak on kozinak get')
    assert_in('fortune', k, 'Invalid json on kozinak get')
    assert_eq(k['fortune'], kozi1['fortune'], 'Invalid kozinak on kozinak get')
    assert_in('owner', k, 'Invalid json on kozinak get')
    assert_eq(k['owner'], "open", 'Invalid kozinak on kozinak get')
    if kozi1.get('pipe') is not None:
        assert_in('pipe', k, 'Invalid json on kozinak get')
        assert_eq(k['pipe'], kozi1['pipe'], 'Invalid kozinak on kozinak get')

    data = mch.register_in_service()
    s = mch.login_in_service(data['username'], data['password'])

    kozi3 = mch.gen_kozi()

    mch.copy_kozinak(s, kozi3['name'], f"http://127.0.0.1:5000/api/kozi/open_{kozi1['name']}/")

    l = mch.list_kozinak()
    assert_in(f"{data['username']}_{kozi3['name']}", l, "Can't copy kozinak")

    k = mch.get_kozinak(s, f"{data['username']}_{kozi3['name']}")

    assert_in('name', k, 'Invalid json on kozinak get after copy')
    assert_eq(k['name'], kozi3['name'], 'Invalid kozinak on kozinak get after copy')
    assert_in('fortune', k, 'Invalid json on kozinak get after copy')
    assert_eq(k['fortune'], kozi1['fortune'], 'Invalid kozinak on kozinak get after copy')
    assert_in('owner', k, 'Invalid json on kozinak get after copy')
    assert_eq(k['owner'], data['username'], 'Invalid kozinak on kozinak get after copy')
    if kozi1.get('pipe') is not None:
        assert_in('pipe', k, 'Invalid json on kozinak get after copy')
        assert_eq(k['pipe'], kozi1['pipe'], 'Invalid kozinak on kozinak get after copy')

    kozi2 = mch.gen_kozi()
    kozi2['pipe'] = f"{data['username']}_{kozi3['name']}"

    mch.create_kozinak(s, kozi2)

    l = mch.list_kozinak()
    assert_in(f"{data['username']}_{kozi2['name']}", l, "Can't add kozinak")

    k = mch.get_kozinak(s, f"{data['username']}_{kozi2['name']}")

    assert_in('name', k, 'Invalid json on kozinak get')
    assert_eq(k['name'], kozi2['name'], 'Invalid kozinak on kozinak get')
    assert_in('fortune', k, 'Invalid json on kozinak get')
    assert_eq(k['fortune'], kozi2['fortune'], 'Invalid kozinak on kozinak get')
    assert_in('owner', k, 'Invalid json on kozinak get')
    assert_eq(k['owner'], data['username'], 'Invalid kozinak on kozinak get')
    if kozi2.get('pipe') is not None:
        assert_in('pipe', k, 'Invalid json on kozinak get')
        assert_eq(k['pipe'], kozi2['pipe'], 'Invalid kozinak on kozinak get')

    kozi4 = mch.gen_kozi()
    kozi4['pipe'] = f"{data['username']}_{kozi2['name']}"

    mch.create_kozinak(s, kozi4)

    l = mch.list_kozinak()
    assert_in(f"{data['username']}_{kozi4['name']}", l, "Can't add kozinak")

    k = mch.get_kozinak(s, f"{data['username']}_{kozi4['name']}")

    assert_in('name', k, 'Invalid json on kozinak get')
    assert_eq(k['name'], kozi4['name'], 'Invalid kozinak on kozinak get')
    assert_in('fortune', k, 'Invalid json on kozinak get')
    assert_eq(k['fortune'], kozi4['fortune'], 'Invalid kozinak on kozinak get')
    assert_in('owner', k, 'Invalid json on kozinak get')
    assert_eq(k['owner'], data['username'], 'Invalid kozinak on kozinak get')
    if kozi4.get('pipe') is not None:
        assert_in('pipe', k, 'Invalid json on kozinak get')
        assert_eq(k['pipe'], kozi4['pipe'], 'Invalid kozinak on kozinak get')

    exec_result = mch.exec_kozinak(s, f"{data['username']}_{kozi4['name']}")

    assert_eq(exec_result, kozi4['fortune'] + kozi2['fortune'] + kozi1['fortune'], 'Invalid exec result')

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
            quit(Status.ERROR, 'System error', 'Unknown action: ' + action)
        
        cquit(Status.ERROR)
    except requests.exceptions.ConnectionError:
        cquit(Status.DOWN, 'Connection error')
    except SystemError as e:
        raise
    except Exception as e:
        cquit(Status.ERROR, 'System error', str(e))