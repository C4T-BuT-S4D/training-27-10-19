from os import system
from helpers import hchecksum
from models import Kozinak, User

def create_kozinak_chk(name, fortune, checksum, owner, pipe=None):
    k = Kozinak(name, fortune, pipe, "tmp")
    k.save()
    h = hchecksum(fortune)
    if h != checksum:
        k.delete()
        return False
    k.delete()
    k.set_owner(owner)
    k.save()
    return True

def create_kozinak(name, fortune, owner, pipe=None):
    k = Kozinak(name, fortune, pipe, owner)
    k.save()

def find_kozinak(fullname):
    try:
        k = Kozinak.load(fullname)
        return k
    except Exception as e:
        pass
    return None

def find_user(username):
    try:
        u = User.load(username)
        return u
    except:
        pass
    return None

def create_user(username, password):
    u = User(username, password)
    u.save()