import email
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class" : "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class" : "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired()], render_kw={"class" : "form-control"})
    org_checkbox = BooleanField('Вы представитель организации?')  # Задел на будущее, пока используем логин, пароль, почту
    submit = SubmitField('Войти', render_kw={"class" : "btn btn-primary"})