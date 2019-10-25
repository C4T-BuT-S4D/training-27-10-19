from helpers import write_response, parse_cookies, get_body, set_cookies, validate, chk_owner
from controllers import find_user, create_user, create_kozinak, find_kozinak, create_kozinak_chk
from session import get_session_manager
from urllib import urlopen
import json
import os

def get_json_or_error(r, w):
    body = get_body(r)
    try:
        d = json.loads(body)
    except ValueError:
        write_response(w, '{"error": "incorrect json"}')
        return None
    return d

def not_found(r, w, params):
    write_response(w, '{"error": "404"}')

def register(r, w, params):
    d = get_json_or_error(r, w)

    if d is None:
        return

    if "username" not in d or "password" not in d:
        write_response(w, '{"error": "no username or password in body"}')
        return

    username = d["username"]
    password = d["password"]

    u = find_user(username)

    if u is not None:
        write_response(w, '{"error": "user already exists"}')
        return

    if not validate(username):
        write_response(w, '{"error": "invalid username or password"}')
        return

    create_user(username, password)

    write_response(w, '{"result": "ok"}')

def login(r, w, params):
    d = get_json_or_error(r, w)

    if d is None:
        return

    if "username" not in d or "password" not in d:
        write_response(w, '{"error": "no username or password in body"}')
        return

    username = d["username"]
    password = d["password"]

    u = find_user(username)

    if u is None:
        write_response(w, '{"error": "no such user"}')
        return

    if u.password != password:
        write_response(w, '{"error": "incorrect password"}')
        return

    mng = get_session_manager()
    session_name = mng.init_session()
    mng.update_session(session_name, username)
    set_cookies(w, { 'session': session_name })
    write_response(w, '{"result": "ok"}')

def list_kozinaks(r, w, params):
    os.chdir("/db/kozi")
    kozi = filter(os.path.isfile, os.listdir("/db/kozi"))
    kozi = [os.path.join("/db/kozi", f) for f in kozi]
    kozi.sort(key=lambda x: os.path.getmtime(x))
    kozi = [f[9:] for f in kozi][::-1]
    write_response(w, json.dumps({
        "result": kozi
    }))

def create_kozi(r, w, params):
    cookies = parse_cookies(r)
    if "session" not in cookies:
        write_response(w, '{"error": "auth is required"}')
        return

    mng = get_session_manager()
    username = mng.get_session(cookies["session"])
    if username is None:
        write_response(w, '{"error": "auth is required"}')
        return

    u = find_user(username)

    if u is None:
        write_response(w, '{"error": "auth is required"}')
        return

    d = get_json_or_error(r, w)

    if d is None:
        return

    if "name" not in d or "fortune" not in d or "checksum" not in d:
        write_response(w, '{"error": "no name or fortune or checksum in body"}')
        return

    name = d["name"]

    if not validate(name):
        write_response(w, '{"error": "invalid name"}')
        return

    k = find_kozinak("%s_%s" % (username, name))

    if k is not None:
        write_response(w, '{"error": "kozinak already exists"}')
        return

    fortune = d["fortune"]
    checksum = d["checksum"]
    pipe = d["pipe"] if "pipe" in d else None

    if create_kozinak_chk(name, fortune, checksum, username, pipe):
        write_response(w, '{"result": "ok"}')
    else:
        write_response(w, '{"error": "incorrect checksum"}')

def get_kozi(r, w, params):
    if len(params) != 1:
        write_response(w, '{"error": "no kozi in params"}')
        return

    kozi_name = params[0]

    k = find_kozinak(kozi_name)

    if k is None:
        write_response(w, '{"error": "no such kozinak"}')
        return

    if k.owner != "open":

        cookies = parse_cookies(r)
        if "session" not in cookies:
            write_response(w, '{"error": "auth is required"}')
            return

        mng = get_session_manager()
        username = mng.get_session(cookies["session"])
        if username is None:
            write_response(w, '{"error": "auth is required"}')
            return

        u = find_user(username)

        if u is None:
            write_response(w, '{"error": "auth is required"}')
            return

        if not chk_owner(username, k.owner):
            write_response(w, '{"error": "no access"}')
            return

    write_response(w, json.dumps({
        'result': json.loads(k.to_json())
    }))

def open_kozi(r, w, params):
    cookies = parse_cookies(r)
    if "session" not in cookies:
        write_response(w, '{"error": "auth is required"}')
        return

    mng = get_session_manager()
    username = mng.get_session(cookies["session"])
    if username is None:
        write_response(w, '{"error": "auth is required"}')
        return

    u = find_user(username)

    if u is None:
        write_response(w, '{"error": "auth is required"}')
        return

    d = get_json_or_error(r, w)

    if d is None:
        return

    if "kozi" not in d:
        write_response(w, '{"error": "no kozi in body"}')
        return

    kozi_name = d["kozi"]

    k = find_kozinak(kozi_name)

    if k is None:
        write_response(w, '{"error": "no such kozinak"}')
        return

    if not chk_owner(username, k.owner):
        write_response(w, '{"error": "no access"}')
        return

    k.delete()
    k.set_owner("open")
    k.save()

    write_response(w, '{"result": "ok"}')

def copy_kozi(r, w, params):
    cookies = parse_cookies(r)
    if "session" not in cookies:
        write_response(w, '{"error": "auth is required"}')
        return

    mng = get_session_manager()
    username = mng.get_session(cookies["session"])
    if username is None:
        write_response(w, '{"error": "auth is required"}')
        return

    u = find_user(username)

    if u is None:
        write_response(w, '{"error": "auth is required"}')
        return

    d = get_json_or_error(r, w)

    if d is None:
        return

    if "url" not in d or "name" not in d:
        write_response(w, '{"error": "no name or url in body"}')
        return

    url = d["url"]
    name = d["name"]

    if not validate(name):
        write_response(w, '{"error": "invalid name"}')
        return

    if url.lower().startswith("gopher") or url.lower().startswith("file"):
        write_response(w, '{"error": "invalid url"}')
        return

    req = urlopen(url)

    data = req.read()

    try:
        j = json.loads(data)
    except:
        write_response(w, '{"error": "incorrect json %s"}' % data)
        return

    if "result" not in j:
        write_response(w, '{"error": "incorrect json %s"}' % data)
        return

    j = j["result"]

    if type(j) != type({}):
        write_response(w, '{"error": "incorrect json %s"}' % data)
        return

    if "name" not in j or "fortune" not in j or "owner" not in j or "pipe" not in j:
        write_response(w, '{"error": "no name or fortune or owner or pipe in body"}')
        return

    fortune = j["fortune"]
    pipe = j["pipe"]

    k = find_kozinak("%s_%s" % (username, name))

    if k is not None:
        write_response(w, '{"error": "kozinak already exists"}')
        return

    create_kozinak(name, fortune, username, pipe)
    write_response(w, '{"result": "ok"}')

def exec_kozi(r, w, params):
    if len(params) != 1:
        write_response(w, '{"error": "no kozi in params"}')
        return

    kozi_name = params[0]

    k = find_kozinak(kozi_name)

    if k is None:
        write_response(w, '{"error": "no such kozinak"}')
        return

    if k.owner != "open":

        cookies = parse_cookies(r)
        if "session" not in cookies:
            write_response(w, '{"error": "auth is required"}')
            return

        mng = get_session_manager()
        username = mng.get_session(cookies["session"])
        if username is None:
            write_response(w, '{"error": "auth is required"}')
            return

        u = find_user(username)

        if u is None:
            write_response(w, '{"error": "auth is required"}')
            return

        if not chk_owner(username, k.owner):
            write_response(w, '{"error": "no access"}')
            return

    result = ""

    while True:
        result += k.fortune
        if k.pipe is not None:
            newk = find_kozinak(k.pipe)
            if newk is not None:
                k = newk
            else:
                break
        else:
            break

    write_response(w, json.dumps({
        'result': result
    }))