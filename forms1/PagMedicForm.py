from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Email, Length, EqualTo, ValidationError

from model import Patient


class PagMedicForm(FlaskForm):
    numeParinte = StringField('Nume', validators=[InputRequired()])
    prenumePatinte = StringField('Prenume', validators=[InputRequired()])
    telefon = IntegerField('Telefon', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email(message="Email invalid"), Length(min=4, max=25)])
    parola = PasswordField('Parolă', validators=[DataRequired(), Length(min=4, max=25)])
    parola2 = PasswordField('Repetă parolă', validators=[DataRequired(), EqualTo('parola'), Length(min=4, max=25)])
    numeCopil = StringField('Nume Copil', validators=[InputRequired()])
    prenumeCopil = StringField('Prenume Copil', validators=[InputRequired()])
    varsta = IntegerField('Varsta Copil', validators=[InputRequired()])
    submit = SubmitField('Creeaza cont ')

    def validate_email(self, email):
        pacient = Patient.query.filter_by(email=email.data).first()
        if pacient is not None:
            raise ValidationError('Te rog foloseste alt email.')