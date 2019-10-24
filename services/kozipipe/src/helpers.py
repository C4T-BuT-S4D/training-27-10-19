from System.Text import Encoding
from hashlib import sha512
from System.Net import Cookie
from System.IO import StreamReader
import re

def write_response(w, text):
    buf = Encoding.UTF8.GetBytes(text)
    w.ContentLength64 = buf.Length
    output = w.OutputStream
    output.Write(buf, 0, buf.Length)
    output.Close()

def get_body(r):
    body = r.InputStream
    encoding = r.ContentEncoding
    reader = StreamReader(body, encoding)
    s = reader.ReadToEnd()
    return s

def hchecksum(text):
    h = text
    for i in range(25000):
        h = sha512(h).hexdigest()
    return h

def validate(text):
    return re.match("[A-Za-z0-9]*", text) != None

def parse_cookies(r):
    c = r.Cookies
    cookies = dict()
    for i in range(c.Count):
        cookies[c[i].Name] = c[i].Value
    return cookies

def set_cookies(w, cookies):
    for c in cookies:
        cook = Cookie(c, cookies[c], "/")
        w.AppendCookie(cook)

def chk_owner(me, owner):
    return me == owner or owner == "tmp" or owner == "open"