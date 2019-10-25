from server import SimpleServer
from router import Router

from views import *

if __name__ == '__main__':
    r = Router()

    r.add_route('/api/register/', register, 'POST')
    r.add_route('/api/login/', login, 'POST')
    r.add_route('/api/list/', list_kozinaks, 'GET')
    r.add_route('/api/kozi/', create_kozi, 'POST')
    r.add_route('/api/copy_kozi/', copy_kozi, 'POST')
    r.add_route('/api/open_kozi/', open_kozi, 'POST')
    r.add_route('/api/kozi/(.+)', get_kozi, 'GET')
    r.add_route('/api/exec_kozi/(.+)', exec_kozi, 'GET')

    s = SimpleServer(r, 5000)
    s.serve()