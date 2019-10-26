import requests
import checklib


class CheckMachine:
    PORT = 5555

    @property
    def url(self):
        return "http://{}:{}".format(self.host, self.PORT)

    def __init__(self, host):
        self.host = host

    def register_service(self, password=None):
        username = checklib.rnd_username()
        if not password:
            password = checklib.rnd_password()
        r = requests.get(f'{self.url}/registerForm', params={'login': username, 'password': password})
        checklib.check_response(r, 'Could not register')
        return username, password

    def login_in_service(self, login, password):
        login_url = f'{self.url}/loginForm'
        session = requests.Session()
        login_data = {
            'login': login,
            'password': password
        }
        r = session.get(url=login_url, params=login_data, allow_redirects=False)
        checklib.assert_eq(r.status_code, 302, "Cant't login in service")
        return session

    def add_icecream(self, session, text):
        add_url = f'{self.url}/addForm'
        r = session.get(url=add_url, params={'icecream': text})
        checklib.check_response(r, 'Could not add icecream')
        return checklib.get_text(r, 'Could not add icecream')

    def get_my_icecreams(self, session):
        my_url = f'{self.url}/icecreams'
        r = session.get(url=my_url)
        checklib.check_response(r, 'Could not get user icecreams')
        return checklib.get_text(r, 'Could not get user icecreams')

    def get_index(self):
        r = requests.get(f'{self.url}/')
        checklib.check_response(r, 'Could not get main page')
        return checklib.get_text(r, 'Could not get main page')

    def get_login_page(self):
        r = requests.get(f'{self.url}/login.html')
        checklib.check_response(r, 'Could not get login page')
        return checklib.get_text(r, 'Could not get login page')

    def get_register_page(self):
        r = requests.get(f'{self.url}/register.html')
        checklib.check_response(r, 'Could not get register page')
        return checklib.get_text(r, 'Could not get register page')

    def get_add_page(self, sess):
        r = sess.get(f'{self.url}/add.html')
        checklib.check_response(r, 'Could not get add icecream page')
        return checklib.get_text(r, 'Could not get add icecream page')

    def get_last_users(self):
        r = requests.get(f'{self.url}/lastusers')
        checklib.check_response(r, 'Could not get last users')
        return checklib.get_text(r, 'Could not get last users')
