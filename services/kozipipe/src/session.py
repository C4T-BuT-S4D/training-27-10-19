from random import choice
from string import ascii_letters

class SessionManager:
    def __init__(self):
        self.sessions = dict()

    def init_session(self):
        session_name = ""
        for i in range(10):
            session_name += choice(ascii_letters)
        self.sessions[session_name] = None
        return session_name

    def get_session(self, session_name):
        return self.sessions.get(session_name)

    def update_session(self, session_name, value):
        self.sessions[session_name] = value

    def destroy_session(self, session_name):
        del self.sessions[session_name]

session_manager = None

def get_session_manager():
    global session_manager
    if session_manager is None:
        session_manager = SessionManager()
    return session_manager