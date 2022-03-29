from dataclasses import fields
import datetime
from webapp.database import db_session
from webapp.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, TextAreaField, TimeField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length, NumberRange


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={"class": "form-control"}
    )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={"class": "form-check-input"}
    )
    submit = SubmitField(
        'Войти',
        render_kw={"class": "btn btn-primary"}
    )


class RegistrationForm(FlaskForm):

    username = StringField(
        'Имя пользователя',
        validators=[
            DataRequired(),
            Length(min=5, max=20, message='Имя должно содержать от 5 до 20 символов!')
        ],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        'Придумайте пароль',
        validators=[
            DataRequired(),
            Length(min=5, max=20, message='Пароль должен содержать содержать от 5 до 20 символов!')
        ],
        render_kw={"class": "form-control"}
    )
    confirm_password = PasswordField(
        'Повторите пароль',
        validators=[
            EqualTo('password', message='Пароли не совпадают'),
            DataRequired(),
            Length(min=5, max=20, message='Пароль должен содержать содержать от 5 до 20 символов!')
        ],
        render_kw={"class": "form-control"}
    )
    email = StringField(
        'Укажите адрес своей электронной почты',
        validators=[
            Email('Некорректный адрес электронной почты')
        ],
        render_kw={"class": "form-control"}
    )
    submit = SubmitField(
        'Зарегистрироваться',
        render_kw={"class": "btn btn-primary"}
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
                'Указанный электронный адрес уже используется другим пользователем.'
            )


class ProfileForm(FlaskForm):

    name = StringField(
        'Имя',
        validators=[
            Length(min=2, message='Имя должно содержать от 2 символов!')
        ],
        render_kw={"class": "form-control", 'placeholder': 'Имя'}
    )
    surname = StringField(
        'Фамилия',
        validators=[
            Length(min=2, message='Фамилия должна содержать от 2 символов!')
        ],
        render_kw={"class": "form-control", 'placeholder': 'Фамилия'}
    )
    email = StringField(
        'Сменить адрес электронной почты',
        validators=[
            Email('Некорректный адрес электронной почты')
        ],
        render_kw={"class": "form-control", 'placeholder': 'Email'}
    )
    country = StringField(
        'Страна',
        render_kw={"class": "form-control", 'placeholder': 'Страна'}
    )
    city = StringField(
        'Город',
        render_kw={"class": "form-control", 'placeholder': 'Город'}
    )
    favorite_games = StringField(
        'Любимые игры',
        render_kw={"class": "form-control", 'placeholder': 'Мои любимые игры'}
    )
    desired_games = StringField(
        'Хочу поиграть',
        render_kw={"class": "form-control", 'placeholder': 'Хочу поиграть в'}
    )
    about_user = StringField(
        'О себе:',
        render_kw={"class": "form-control", 'placeholder': 'Обо мне:'}
    )
    submit = SubmitField(
        'Сохранить',
        render_kw={"class": "btn btn-primary"}
    )


class MeetingForm(FlaskForm):
    game_name = StringField(
        'Введите название игры в которую хотите поиграть.',
        validators=[
            DataRequired(),
        ],
        render_kw={"class": "form-control"},
        id='game_autocomplete'
    )
    number_of_players = IntegerField(
        'Укажите количество игроков, которых Вы хотите найти.',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=50, message="Нужно указать значение от 1 до 50")
        ],
        render_kw={"class": "form-control", 'placeholder': 'От 1 до 50 игроков'}
    )
    meeting_place = StringField(
        'Укажите место встречи.',
        validators=[
            DataRequired(),
        ],
        render_kw={"class": "form-control", 'placeholder': 'г. Москва, Парк Останкино, 2-я лавочка от входа'}
    )
    date_meeting = DateField(
        'Выберите дату встречи.',
        validators=[
            DataRequired(),
        ],
        render_kw={"class": "form-control"}
    )
    time_meeting = TimeField(
        'Выберите время встречи.',
        validators=[
            DataRequired(),
        ],
        render_kw={"class": "form-control"}
    )
    description = TextAreaField(
        'Тут можно указать любую дополнительную информацию.',
        render_kw={"class": "form-control", 'placeholder': 'Например: играю только с девчонками и на раздевание'}
    )
    submit = SubmitField(
        'Сохранить',
        render_kw={"class": "btn btn-primary"}
    )

    def validate_date_meeting(self, date_meeting: fields) -> None:
        """Запрещает выбрать прошедшую дату"""
        if date_meeting.data < datetime.date.today():
            raise ValidationError("Дата не может быть в прошлом!")

    def validate_time_meeting(self, time_meeting :fields) -> None:
        """Если выбран текущий день, то запрещает выбрать прошедшее время"""
        if self.date_meeting.data == datetime.date.today():
            if time_meeting.data < datetime.datetime.now().time():
                raise ValidationError("Время не может быть в прошлом!")


class ButtonForm(FlaskForm):
    current_meet = IntegerField()

    submit_add_wish = SubmitField(
        'Участвовать',
        render_kw={"class": "btn btn-primary"}
    )
    submit_del = SubmitField(
        'Покинуть встречу',
        render_kw={"class": "btn btn-primary"}
    )
    submit_edit = SubmitField(
        'Редактировать встречу в профиле',
        render_kw={"class": "btn btn-primary"}
    )
