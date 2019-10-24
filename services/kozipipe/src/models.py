from os import remove
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        filename = "/db/users/%s" % self.username
        content = self.to_json()
        with open(filename, "w") as w:
            w.write(content)

    def delete(self):
        filename = "/db/users/%s" % self.username
        system("rm %s" % filename)

    @classmethod
    def load(cls, username):
        with open("/db/users/%s" % username, "r") as r:
            j = json.loads(r.read())
        return cls.from_json(j)

    def to_json(self):
        return json.dumps({
            'username': self.username,
            'password': self.password,
        })

    @classmethod
    def from_json(cls, j):
        return cls(j['username'], j['password'])


class Kozinak:
    def __init__(self, name, fortune, pipe, owner):
        self.name = name
        self.fortune = fortune
        self.pipe = pipe
        self.owner = owner

    def set_owner(self, owner):
        self.owner = owner

    def save(self):
        filename = "/db/kozi/%s_%s" % (self.owner, self.name)
        content = self.to_json()
        with open(filename, "w") as w:
            w.write(content)

    def delete(self):
        filename = "/db/kozi/%s_%s" % (self.owner, self.name)
        remove(filename)

    @classmethod
    def load(cls, fullname):
        with open("/db/kozi/%s" % fullname, "r") as r:
            j = json.loads(r.read())
        return cls.from_json(j)

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'fortune': self.fortune,
            'pipe': self.pipe,
            'owner': self.owner,
        })

    @classmethod
    def from_json(cls, j):
        return cls(j['name'], j['fortune'], j['pipe'], j['owner'])
