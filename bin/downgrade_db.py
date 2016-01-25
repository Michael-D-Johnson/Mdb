#!/usr/bin/env python

from Mdb import Mdb
from migrate.versioning import api

SQLALCHEMY_DATABASE_URI = Mdb.config['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_MIGRATE_REPO = Mdb.config['SQLALCHEMY_MIGRATE_REPO']

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))
