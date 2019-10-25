import base64
import re
import requests
from checklib import *

PORT = 8001

class CheckMachine:

    @property
    def url(self):
        return f'http://{self.host}:{self.port}'

    def __init__(self, host):
        self.host = host
        self.port = PORT

    @staticmethod
    def get_name_regex(model):
        model_name = model.capitalize()
        return f'<td>\W*(\w+)\W*</td>\s*<td>\s*<a href="/{model_name}/View{model_name}/\d+"'

    @staticmethod
    def get_id_regex(model):
        model_name = model.capitalize()
        return f'<td>\W*\w+\W*</td>\s*<td>\s*<a href="/{model_name}/View{model_name}/(\d+)"'

    def register_user(self):
        username = rnd_username()
        password = rnd_password()

        r = requests.post(f'{self.url}/User/RegisterPost', data={'username': username, 'password': password})
        check_response(r, 'Could not register')
        return username, password

    def login_user(self, username, password):
        sess = get_initialized_session()

        r = sess.post(f'{self.url}/User/LoginPost', data={'username': username, 'password': password})
        check_response(r, 'Could not login')

        return sess

    def get_index(self, sess):
        r = sess.get(f'{self.url}/')
        check_response(r, 'Could not get main page')
        return get_text(r, 'Could not get main page')

    def get_me(self, sess):
        r = sess.get(f'{self.url}/User/Me')
        check_response(r, 'Could not get Me')
        return get_text(r, 'Could not get Me')

    def get_user_page(self, sess, user_id):
        r = sess.get(f'{self.url}/User/ViewUser/{user_id}')
        check_response(r, 'Could not get user page')
        return get_text(r, 'Could not get user page')

    def get_users(self, sess):
        r = sess.get(f'{self.url}/User/List')
        check_response(r, 'Could not get user list')
        page = get_text(r, 'Could not get user list')
        names = re.findall(self.get_name_regex('user'), page, re.DOTALL)
        ids = re.findall(self.get_id_regex('user'), page, re.DOTALL)
        assert_eq(len(ids), len(names), 'Id count not matching name count')
        return ids, names

    def add_chocolate(self, sess, name, description):
        r = sess.post(f'{self.url}/Chocolate/CreatePost', data={'name': name, 'description': description})
        check_response(r, 'Could not create chocolate')

    def add_wrapper(self, sess, name):
        r = sess.post(f'{self.url}/Wrapper/CreatePost', data={'name': name})
        check_response(r, 'Could not create wrapper')

    def get_my_chocolates(self, sess):
        me = self.get_me(sess)
        names = re.findall(self.get_name_regex('chocolate'), me, re.DOTALL)
        ids = re.findall(self.get_id_regex('chocolate'), me, re.DOTALL)
        assert_eq(len(ids), len(names), 'Id count not matching name count')
        return ids, names

    def get_my_friends(self, sess):
        me = self.get_me(sess)
        names = re.findall(self.get_name_regex('user'), page, re.DOTALL)
        ids = re.findall(self.get_id_regex('user'), page, re.DOTALL)
        assert_eq(len(ids), len(names), 'Id count not matching name count')
        return ids, names

    def get_my_wrappers(self, sess):
        me = self.get_me(sess)
        names = re.findall(self.get_name_regex('wrapper'), me, re.DOTALL)
        ids = re.findall(self.get_id_regex('wrapper'), me, re.DOTALL)
        assert_eq(len(ids), len(names), 'Id count not matching name count')
        return ids, names

    def make_friends(self, sess, user_id, guesses):
        r = sess.post(f'{self.url}/User/AddToFriends', data={'id': user_id, 'guesses': guesses})
        check_response(r, 'Could not add a friend')

    def get_user_chocolates(self, sess, user_id):
        me = self.get_user_page(sess, user_id)
        names = re.findall(self.get_name_regex('chocolate'), me, re.DOTALL)
        ids = re.findall(self.get_id_regex('chocolate'), me, re.DOTALL)
        assert_eq(len(ids), len(names), 'Id count not matching name count')
        return ids, names

    def get_chocolate(self, sess, choco_id):
        r = sess.get(f'{self.url}/Chocolate/ViewChocolate/{choco_id}')
        check_response(r, 'Could not get chocolate')
        return get_text(r, 'Could not get chocolate')

    def get_wrapper(self, sess, wrapper_id):
        r = sess.get(f'{self.url}/Wrapper/ViewWrapper/{wrapper_id}')
        check_response(r, 'Could not get wrapper')
        return get_text(r, 'Could not get wrapper')
