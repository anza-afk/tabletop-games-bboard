from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={"class" : "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class" : "form-control"}
    )
    submit = SubmitField(
        'Войти',
        render_kw={"class" : "btn btn-primary"}
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={"class" : "form-control"}
        )
    password = PasswordField(
        'Придумайте пароль',
        validators=[DataRequired()],
        render_kw={"class" : "form-control"}
        )
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[EqualTo('password', message='Пароли не совпадают'), DataRequired()],
        render_kw={"class" : "form-control"}
        )
    email = StringField(
        'Укажите адрес своей электронной почты',
        validators=[DataRequired()],
        render_kw={"class" : "form-control"}
        )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={"class" : "btn btn-primary"}
        )