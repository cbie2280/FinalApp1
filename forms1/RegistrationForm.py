from flask_wtf import FlaskForm
from model.Medic import Medic
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError


class RegistrationForm(FlaskForm):
    nume = StringField('Nume', validators=[InputRequired()])
    prenume = StringField('Prenume', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message="Email invalid"), Length(min=4, max=25)])
    parola = PasswordField('Parolă', validators=[DataRequired(), Length(min=4, max=25)])
    parola2 = PasswordField('Repetă parolă', validators=[DataRequired(), EqualTo('parola'), Length(min=4, max=25)])
    submit = SubmitField('Creează')

    def validate_email(self, email):
        medic = Medic.query.filter_by(email=email.data).first()
        if medic is not None:
            raise ValidationError('Te rog foloseste alt email.')
