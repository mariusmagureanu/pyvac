__author__ = 'mariusmagureanu'
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf import Form


class LoginForm(Form):
    user_name = StringField('user_name', validators=[DataRequired()])
    user_pass = StringField('user_pass', validators=[DataRequired()])
