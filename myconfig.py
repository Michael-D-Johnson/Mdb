import os

basedir = os.environ.get('MDB_DIR')

DB_DIR = os.path.join(basedir,'db')
SHEETS_DIR = os.path.join(basedir,'sheets')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_DIR, 'members.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(DB_DIR, 'repository')

SECRET_KEY = 'CCCC!$!$AAABBB'

MDB_SERVER= os.getenv('MDB_SERVER')

# Mail settings
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = [MAIL_USERNAME]
