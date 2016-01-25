from flask import render_template,request,redirect,session,url_for
from forms import LoginForm
from Mdb import Mdb
from functools import wraps
from Mdb.models import Profile,Member
import pandas

@Mdb.route('/')
@Mdb.route('/index')
def index():   
    return render_template('index.html')

@Mdb.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        check_user = Profile.query.filter_by(username=form.username.data,
                                             passwd=form.passwd.data).first()
        if check_user:
            session['user_id'] = check_user.id
            session['username'] = check_user.username
            session['logged_in'] = True
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html',form=form)
    
@Mdb.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    return redirect(url_for('index'))

@Mdb.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@Mdb.route('/members_list')
def members_list():
    members = Member.query.with_entities(Member.last_name,
                                         Member.first_name,Member.email,Member.paid).all()
    df = pandas.DataFrame(members,columns=['Last name','First name','Email','Member since'])
    df = df.sort(columns=['Last name'],ascending=True)
    columns = df.columns

    return render_template('members_list.html',columns=columns,df = df)
