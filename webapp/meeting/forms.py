from dataclasses import fields
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField, TextAreaField, TimeField, SelectField
from wtforms.validators import DataRequired, ValidationError, NumberRange


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
    meeting_city = StringField(
        'Укажите город встречи.',
        validators=[
            DataRequired(),
        ],
        render_kw={"class": "form-control", 'placeholder': 'г. Москва'},
        id='city_autocomplete'
    )
    meeting_place = StringField(
        'Укажите адрес встречи.',
        validators=[
            DataRequired(),
        ],
        render_kw={"class": "form-control", 'placeholder': 'ул. Тимирязевская, Бургер кинг'}
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
        render_kw={"class": "form-control", 'placeholder': 'Например: играю только с девчонками и на раздевание'},
        id='meet_description'
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
        'Редактировать встречу',
        render_kw={"class": "btn btn-primary"}
    )


class AvatarForm(FlaskForm):
    choose_avatar = SelectField(
        'Выберите аватар'
    )
    submit = SubmitField(
        'Сменить',
        render_kw={"class": "btn btn-primary"}
    )
