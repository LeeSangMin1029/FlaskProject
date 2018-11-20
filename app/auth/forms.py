from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField
from wtforms.validators import Required, Length, Email

class LoginForm(FlaskForm):
    email=StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password=PasswordField('Password', validators=[Required()])
    check=BooleanField('Keep me logged in')
    submit=SubmitField('Log In')