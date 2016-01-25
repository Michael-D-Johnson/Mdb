from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,PasswordField,SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    username = StringField('Username',validators=[Required()])
    passwd = PasswordField('Password',validators=[Required()])
    submit = SubmitField('Log In')
