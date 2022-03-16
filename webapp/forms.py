from dataclasses import fields
from webapp.db import db_session
from webapp.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class" : "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class" : "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired()], render_kw={"class" : "form-control"})
    org_checkbox = BooleanField('Вы представитель организации?')  # Задел на будущее, пока используем логин, пароль, почту
    submit = SubmitField('Войти', render_kw={"class" : "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(),
            Length(min=5, max=20, message='Имя должно содержать от 5 до 20 символов!')
            ],
        render_kw={"class" : "form-control"}
        )
    password = PasswordField(
        'Придумайте пароль',
        validators=[
            DataRequired(),
            Length(min=5, max=20, message='Пароль должен содержать содержать от 5 до 20 символов!')
            ],
        render_kw={"class" : "form-control"}
        )
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[
            EqualTo('password', message='Пароли не совпадают'),
            DataRequired(),
            Length(min=5, max=20, message='Пароль должен содержать содержать от 5 до 20 символов!')
            ],
        render_kw={"class" : "form-control"}
        )
    email = StringField(
        'Укажите адрес своей электронной почты',
        validators=[
            Email('Некорректный адрес электронной почты')
            ],
        render_kw={"class" : "form-control"}
        )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={"class" : "btn btn-primary"}
        )

    def validate_username(self, username: fields) -> None:
        """
        Проверяет наличие пользователя в БД по имени
        """
        if db_session.query(User.username).filter(User.username == username.data).count():
            raise ValidationError(
                f'Пользователь с именем {username.data} уже существует.'
            )

    def validate_email(self, email: fields) -> None:
        """
        Проверяет наличие пользователя в БД по email
        """
        if db_session.query(User.email).filter(User.email == email.data).count():
            raise ValidationError(
                f'Указанный электронный адрес уже используется другим пользователем.'
            )

