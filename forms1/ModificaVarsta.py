from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import InputRequired


class ModificaVarsta(FlaskForm):
    varsta = IntegerField('Vârstă nouă', validators=[InputRequired()])
    submit = SubmitField('Modifică ')
