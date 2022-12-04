from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.validators import ValidationError
from .models import UserModel


class UserRegisterForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    password1 = PasswordField('Пароль:', validators=[Length(min=8), DataRequired(), EqualTo('password2', 'Пароли должны совпадать')])
    password2 = PasswordField('Подтверждение пароля:', validators=[DataRequired()])

    def validate_username(form, field):
        user = UserModel.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Пользователь с таким именем уже существует')


class UserLoginForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[Length(min=8), DataRequired()])
