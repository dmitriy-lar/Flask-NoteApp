from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired


class NoteCreationForm(FlaskForm):
    title = StringField('Название:', validators=[DataRequired()])
    description = TextAreaField('Описание:')
