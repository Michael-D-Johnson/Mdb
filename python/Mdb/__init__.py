#!/usr/bin/env python

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

Mdb = Flask(__name__,template_folder="../../templates")
Mdb.config.from_envvar('MDB_CONFIG')
Mdb.secret_key = Mdb.config['SECRET_KEY']
db = SQLAlchemy(Mdb)

mail = Mail(Mdb)

from Mdb import models,views

