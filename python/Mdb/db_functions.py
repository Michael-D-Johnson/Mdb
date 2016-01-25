from Mdb import Mdb,models,db
from datetime import timedelta,datetime
from flask import render_template
from emails import send_email
from utils import write_deleted_log
import re

# Grab tablenames from models.py 
from inspect import isclass
tables = [getattr(models,x) for x in dir(models) if isclass(getattr(models,x))]
form_table = tables[0]
member_table = tables[1]
profile_table = tables[2]

def has_paid(name=False):
    """ Returns list of all paid members"""
    # Query for paid members
    ispaid = form_table.query.filter_by(paid=1)

    # Create list from paid members
    paid_list = [i.__dict__ for i in ispaid]

    # Return paid list
    if name is True:
        return [' '.join([i.first_name,i.last_name]) for i in ispaid]
    else:
        return paid_list

def hasnt_paid(name=False):
    """ Returns list of all members not paid"""
    # Query for unpaid members
    isntpaid = form_table.query.filter_by(paid=0).all()
    
    # Create list from unpaid members
    nopay_list = [i.__dict__ for i in isntpaid]
    
    # Return unpaid list
    if name is True:
        return [' '.join([i.first_name,i.last_name]) for i in isntpaid]
    else:
        return nopay_list

def query_all(table,**kwargs):
    """ Returns entire members table"""
    # Query all members
    all = table.query.all()
    
    # Create list from all members
    q_list = [i.__dict__ for i in all]
    
    # Return all members list
    return q_list

def bulk_form_upload(df,db):
    """ Take dataframe and insert into table"""
	df.to_sql(form_table.__tablename__,con=db.engine,if_exists='append',index=False)
def bulk_member_upload(df,db):
    """ Take dataframe and insert into table"""
	df.to_sql(member_table.__tablename__,con=db.engine,if_exists='append',index=False)

def does_form_exist_in_members(df,**kwargs):
    """ Download form spreadsheet. If person doesn't exist in members add to form"""
    # Convert dataframe to dictionary
    df_dict = df.to_dict(orient='records')
    for dict in df_dict: 
        # Query for email
        email_search = form_table.query.filter_by(email=dict['email'])
        exists = [i.__dict__ for i in email_search]
        if exists:
            # if person exists in form do not add
            continue
        elif not exists:
            # if person exists in form make sure they don't also exist in members
            email_search = member_table.query.filter_by(email=dict['email'])
            exists_in_members = [i.__dict__ for i in email_search]
            if exists_in_members:
                # do nothing if person exists in members table
                print "%s %s exists in member table!" % (dict['first_name'],dict['last_name'])
                continue
            else:
                # add to forms table if they do not exist in members
                print "adding %s %s to form" % (dict['first_name'],dict['last_name'])
                add_person = form_table(**dict)
                db.session.add(add_person)
    db.session.commit()

def add_new_member(**kwargs):
    """ Add newly paid members to members table"""
    # Query for all paid members
    ispaid_list = has_paid(form_table)
    for dict in ispaid_list:
        year = datetime.strptime(dict['timestamp'],"%m/%d/%Y %H:%M:%S")
        plusone = (year + timedelta(days=365)).date()
        # Remove dictionary keys not needed for insertion
        del dict['_sa_instance_state']
        del dict['id']
        del dict['timestamp']
        # Add date paid and expired to dictionary
        dict['expires'] = str(plusone)
        dict['paid'] = str(year.date())
        email_search = member_table.query.filter_by(email=dict['email'])  
        exists = [i for i in email_search]
        if len(exists) ==0:
            print "adding %s %s to member" % (dict['first_name'],dict['last_name'])
            new_member = member_table(**dict)
            profile_dict = add_profile(dict)
            new_profile = profile_table(**profile_dict)
            db.session.add(new_member)
            db.session.add(new_profile)
    db.session.commit()

def delete_from_form(**kwargs):
    """ Delete from form table if exists in members"""
    q_list = query_all(member_table)
    for dict in q_list:
        email_search = form_table.query.filter_by(email=dict['email']).first()
        if email_search: 
            print "deleting %s %s from form table" % (dict['first_name'],dict['last_name'])
            db.session.delete(email_search)
    db.session.commit()

def is_expired(**kwargs):
    q_list = query_all(member_table)
    today = datetime.now().date()
    fourweeks = timedelta(days=14)
    for dict in q_list:
        expires = datetime.strptime(dict['expires'],"%Y-%m-%d")
        delete_fil = (expires + fourweeks).date()
        if expires.date() - today == timedelta(days=14):
            with Mdb.test_request_context("/"):
                send_email("Your CUAS membership will expire in two weeks!", Mdb.config['ADMINS'][0],
                    [str(dict['email'])], render_template("will_expire_email.txt",member=str(dict['first_name'])))
        if today == expires.date():
            with Mdb.test_request_context("/"):
                send_email("Your CUAS membership has expired!", Mdb.config['ADMINS'][0],
                    [str(dict['email'])], render_template("expired_email.txt",member=str(dict['first_name'])))
        if today > delete_fil:
            email_search = member_table.query.filter_by(email=dict['email']).first()
            if email_search:
                db.session.delete(email_search)
                write_deleted_log(dict)
                print "%s has been deleted from member table. Membership expired on %s. Log here: %s" % (' '.join([dict['first_name'],dict['last_name']]),expires.date(),"/Users/mjohns44/Code/GIT/Mdb/logs/delete.log")
            db.session.commit() 

def add_profile(dict):
        member_email=dict['email']
        username = dict['last_name'][0:4].lower() + 'test'
        i = 1
        while profile_table.query.filter_by(username=username).first():
            if re.search('\d',username):
                username = re.sub('\d',str(i),username)
            else:
                username = username + str(i)
            i += 1
        new_member= profile_table(member_email=member_email,username=username,passwd='cygnus1')
        return {'member_email':member_email,'username':username,'passwd':'cygnus1'}

def define_passwd():
    """ ? """
    q_list = query_all(member_table)
    for dict in q_list:
        member_email=dict['email']
        username = dict['last_name'][0:4].lower() + 'test'
        i = 1
        while profile_table.query.filter_by(username=username).first():
            if re.search('\d',username):
                username = re.sub('\d',str(i),username)
            else:
                username = username + str(i)
            i += 1
        new_member= profile_table(member_email=member_email,username=username,passwd='cygnus1')
        db.session.add(new_member)
    db.session.commit()
