#!/usr/bin/env python

from migrate.versioning import api
from Mdb import Mdb,db

SQLALCHEMY_DATABASE_URI = Mdb.config['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_MIGRATE_REPO = Mdb.config['SQLALCHEMY_MIGRATE_REPO']

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
