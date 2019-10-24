from server import SimpleServer
from router import Router

from views import *

if __name__ == '__main__':
    r = Router()

    r.add_route('/register/', register, 'POST')
    r.add_route('/login/', login, 'POST')
    r.add_route('/list/', list_kozinaks, 'GET')
    r.add_route('/kozi/', create_kozi, 'POST')
    r.add_route('/copy_kozi/', copy_kozi, 'POST')
    r.add_route('/open_kozi/', open_kozi, 'POST')
    r.add_route('/kozi/(.+)', get_kozi, 'GET')
    r.add_route('/exec_kozi/(.+)', exec_kozi, 'GET')

    s = SimpleServer(r, 5000)
    s.serve()