import os
from datetime import datetime
import textwrap

def write_deleted_log(dict,path="/Users/mjohns44/Code/GIT/Mdb/logs"):
    """ write log """
    now = datetime.now()
    fullname =' '.join([dict['first_name'],dict['last_name']])
    logfile = "delete.log" 
    fullpath = os.path.join(path, logfile)
    with open(fullpath,"a") as deletelog:
        statement = """%s: %s from members. Expiration date: %s.
                    \ndict=%s\n""" % (now,fullname,dict['expires'],dict)
        deletelog.write(textwrap.dedent(statement))
