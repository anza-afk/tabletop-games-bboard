from werkzeug.security import generate_password_hash
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from news_parser.test_parser import result_news
from webapp.forms import LoginForm, RegistrationForm, ProfileForm, MeetingForm
from webapp.users import add_user, add_profile, join_profile, add_profile, update_profile, add_meeting
from webapp.models import User, User_profile, Meeting
from datetime import date
from flask_migrate import Migrate
import webapp.db as db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.errorhandler(500)
    def server_error():
        title = 'Ошибка получения данных'
        return render_template('server_error.html', page_title=title), 500

    @app.route('/')
    def index():
        title = 'Поиск напарников для настольных игр'
        return render_template('index.html', page_title=title, list_news=result_news)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Успешный вход')
                return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/registration', methods=['POST', 'GET'])
    def registration():
        """
        При GET запросе возвращает страницу для регистрации.
        При POST запросе, в случае успешной валидации сохраняет
        нового пользователя в БД.
        """
        title = 'Регистрация'
        registration_form = RegistrationForm()

        if registration_form.validate_on_submit():
            hash_pass = generate_password_hash(registration_form['password'].data)
            new_user = User(
                username=registration_form['username'].data,
                password=hash_pass,
                email=registration_form['email'].data,
                role='1'
                )

            if add_user(new_user):
                flash('Вы успешно зарегистрировались!')
                return redirect(url_for('login'))

            flash('Ошибка регистрации, попробуйте повторить позже.')

        return render_template('registration.html', page_title=title, form=registration_form)

    @login_required
    @app.route('/profile')
    def profile():
        title = f'Профиль {current_user.username}'
        profile_data = join_profile(current_user.id)
        profile_form = ProfileForm()
        return render_template('profile.html', page_title=title, form = profile_form, profile_data = profile_data)

    @app.route('/submit_profile', methods=['POST', 'GET'])
    def submit_profile():
        form = ProfileForm()

#        if form.validate_on_submit():
        if bool(User_profile.query.filter_by(owner_id=current_user.id).first()):
            update_profile(form, current_user)
            flash('Личные данные успешно сохранены!')
            return redirect(url_for('profile'))
        new_profile = User_profile(
            owner_id=current_user.id,
            name=form['name'].data,
            surname=form['surname'].data,
            country=form['country'].data,
            city=form['city'].data,
            favorite_games=form['favorite_games'].data,
            desired_games=form['desired_games'].data,
            about_user=form['about_user'].data
        )

        #  email_for_user = User()
        add_profile(new_profile)
        flash('Личные данные успешно сохранены!')
        return redirect(url_for('profile'))

    @login_required
    @app.route('/create_meeting', methods=['POST', 'GET'])
    def create_meeting():
        """
        При GET запросе возвращает страницу для создания встречи.
        При POST запросе, в случае успешной валидации сохраняет
        новую встречу в БД.
        """
        title = 'Создание встречи'
        meeting_form = MeetingForm()

        if meeting_form.validate_on_submit():
            new_meeting = Meeting(
                game_name = meeting_form['game_name'].data,
                owner_id = current_user.id,
                date_create = date.today(),
                number_of_players = meeting_form['number_of_players'].data,
                meeting_place = meeting_form['meeting_place'].data,
                date_meeting = meeting_form['date_meeting'].data,
                time_meeting = meeting_form['time_meeting'].data,
                description = meeting_form['description'].data
                )

            if add_meeting(new_meeting):
                flash('Вы успешно создали встречу!')
                return redirect(url_for('index'))  # в Дальнейшем на страницу со всеми встречами

            flash('Ошибка создания встречи, попробуйте повторить позже.')

        return render_template('create_meeting.html', page_title=title, form=meeting_form)


    @login_required
    @app.route('/meets', methods=['POST', 'GET'])
    def meets():
        meets_list = db.db_session.query.join(User_profile, User_profile.owner_id == Meeting.owner_id).all()
        for meet in meets_list:
            print(meet.user.username)
            print(meet.city)
        return render_template('meets.html', meets_list=meets_list)
    return app
