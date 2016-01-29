import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.sb'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = '\x1f\xd5W2V\xae\xad\xe3\xe5\xb4Z\xddX\x14\x14\xb8"\x8cx\x94\xb99\xfaG'

DATABASE_PATH = os.path.join(basedir, DATABASE)
