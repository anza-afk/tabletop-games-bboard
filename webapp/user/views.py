from werkzeug.security import generate_password_hash
from flask import Blueprint, redirect, render_template, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
from webapp.user.forms import LoginForm, RegistrationForm, ProfileForm
from webapp.meeting.forms import ButtonForm, AvatarForm
from webapp.users import add_user, add_profile, join_profile, update_profile, owner_meetings, sub_to_meetings
from webapp.user.models import User, UserProfile
from webapp.meeting.models import MeetingUser, GameMeeting
from webapp.database import db_session
import os

blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='static')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Успешный вход')
            return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@blueprint.route('/registration', methods=['POST', 'GET'])
def registration():
    """
    При GET запросе возвращает страницу для регистрации.
    При POST запросе, в случае успешной валидации сохраняет
    нового пользователя в БД.
    """
    title = 'Регистрация'
    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():
        hash_pass = generate_password_hash(
            registration_form['password'].data
        )
        new_user = User(
            username=registration_form['username'].data,
            password=hash_pass,
            email=registration_form['email'].data,
            role='1'
        )

        if add_user(new_user):
            flash('Вы успешно зарегистрировались!')
            return redirect(url_for('user.login'))

        flash('Ошибка регистрации, попробуйте повторить позже.')

    return render_template(
        'registration.html',
        page_title=title,
        form=registration_form
    )


@blueprint.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    title = f'Профиль {current_user.username}'

    buttons = ButtonForm()
    avatar_form = AvatarForm()
    print(blueprint.static_folder)
    img_dict = os.listdir(os.path.join(blueprint.static_folder, "images/avatars"))
    avatar_form.choose_avatar.choices = [(f'static/images/avatars/{img}', img, ) for img in img_dict]

    if buttons.validate_on_submit():
        with db_session() as session:
            player = session.query(MeetingUser).join(GameMeeting).filter(
                GameMeeting.id == buttons.current_meet.data
            ).filter(
                MeetingUser.meeting_id == GameMeeting.id
            ).filter(MeetingUser.user_id == current_user.id).one()
            session.delete(player)
            session.commit()
        return redirect(url_for('user.profile'))

    profile_data = join_profile(current_user.id)
    meets_data = owner_meetings(current_user.id).order_by(GameMeeting.meeting_date_time.asc())
    meets_user = sub_to_meetings(current_user.id).order_by(GameMeeting.meeting_date_time.asc())
    return render_template(
        'profile.html',
        page_title=title,
        profile_data=profile_data,
        meets_data=meets_data,
        meets_user=meets_user,
        buttons=buttons,
        img_dict=img_dict,
        avatar_form=avatar_form
    )


@blueprint.route('/change_avatar', methods=['POST', 'GET'])
@login_required
def change_avatar():
    avatar_form = AvatarForm()
    with db_session() as session:
        profile = session.query(UserProfile).filter(UserProfile.owner_id == current_user.id).first()
        profile.avatar = avatar_form['choose_avatar'].data
        print(profile.owner_id, '-->', profile.avatar)
        session.commit()
    flash('Личные данные успешно сохранены!')
    return redirect(url_for('user.profile'))


@blueprint.route('/edit_profile')
@login_required
def edit_profile():
    title = f'Профиль {current_user.username}'
    profile_data = join_profile(current_user.id)
    profile_form = ProfileForm()
    return render_template(
        'edit_profile.html',
        page_title=title,
        form=profile_form,
        profile_data=profile_data
    )


@blueprint.route('/submit_profile', methods=['POST', 'GET'])
def submit_profile():
    form = ProfileForm()
    if bool(UserProfile.query.filter_by(owner_id=current_user.id).first()):
        update_profile(form, current_user)
        flash('Личные данные успешно сохранены!')
        return redirect(url_for('user.profile'))
    new_profile = UserProfile(
        owner_id=current_user.id,
        name=form['name'].data,
        surname=form['surname'].data,
        country=form['country'].data,
        city=form['city'].data,
        favorite_games=form['favorite_games'].data,
        desired_games=form['desired_games'].data,
        about_user=form['about_user'].data
    )

    add_profile(new_profile)
    flash('Личные данные успешно сохранены!')
    return redirect(url_for('user.profile'))
