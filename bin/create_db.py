#! /usr/bin/env python
from migrate.versioning import api
from Mdb import Mdb,db
import os.path

SQLALCHEMY_DATABASE_URI = Mdb.config['SQLALCHEMY_DATABASE_URI']
SQLALCHEMY_MIGRATE_REPO = Mdb.config['SQLALCHEMY_MIGRATE_REPO']

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
