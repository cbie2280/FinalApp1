from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message="Email invalid"), Length(min=4, max=25)])
    password = PasswordField('Parolă', validators=[InputRequired(), Length(min=4, max=25)])
    remember = BooleanField('Ține-mă minte!')
    submit = SubmitField('Conectare')
