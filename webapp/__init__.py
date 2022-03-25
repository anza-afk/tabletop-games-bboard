from datetime import date
from doctest import REPORTING_FLAGS
from werkzeug.security import generate_password_hash
from flask import Flask, redirect, render_template, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from news_parser.test_parser import result_news
import webapp.db as db
from webapp.forms import LoginForm, RegistrationForm, ProfileForm, MeetingForm, ButtonForm
from webapp.users import add_user, add_profile, join_profile, update_profile, add_meeting, paginate
from webapp.models import User, UserProfile, Meeting
from webapp.config import GAMES_PER_PAGE
from math import ceil

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Для доступа на эта страницу необходимо авторизоваться!'
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
                return redirect(url_for('login'))

            flash('Ошибка регистрации, попробуйте повторить позже.')

        return render_template(
            'registration.html',
            page_title=title,
            form=registration_form
        )

    
    @app.route('/profile')
    @login_required
    def profile():
        title = f'Профиль {current_user.username}'
        profile_data = join_profile(current_user.id)
        profile_form = ProfileForm()
        return render_template(
            'profile.html',
            page_title=title,
            form=profile_form,
            profile_data=profile_data
        )

    @app.route('/submit_profile', methods=['POST', 'GET'])
    def submit_profile():
        form = ProfileForm()

#        if form.validate_on_submit():
        if bool(UserProfile.query.filter_by(owner_id=current_user.id).first()):
            update_profile(form, current_user)
            flash('Личные данные успешно сохранены!')
            return redirect(url_for('profile'))
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

        #  email_for_user = User()
        add_profile(new_profile)
        flash('Личные данные успешно сохранены!')
        return redirect(url_for('profile'))

   
    @app.route('/create_meeting', methods=['POST', 'GET'])
    @login_required
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
                game_name=meeting_form['game_name'].data,
                owner_id=current_user.id,
                date_create=date.today(),
                number_of_players=meeting_form['number_of_players'].data,
                meeting_place=meeting_form['meeting_place'].data,
                date_meeting=meeting_form['date_meeting'].data,
                time_meeting=meeting_form['time_meeting'].data,
                description=meeting_form['description'].data,
                wishing_to_play=[],
                confirmed_players=[],
                )
            if add_meeting(new_meeting):
                flash('Вы успешно создали встречу!')
                return redirect(url_for('index'))

            flash('Ошибка создания встречи, попробуйте повторить позже.')

        return render_template(
            'create_meeting.html',
            page_title=title,
            form=meeting_form
        )


    @app.route('/meets', methods=['POST', 'GET'])
    @app.route('/meets/<int:page>', methods=['POST', 'GET'])
    @login_required 
    def meets(page=1):
        title = 'LFG'
        buttons = ButtonForm()

        if buttons.validate_on_submit():
            if buttons.submit_add_wish.data:
                with db.db_session() as session:
                    meet = session.query(Meeting).filter(Meeting.id == buttons.current_meet.data).first()
                    meet.add_user(current_user.id)
                    session.commit()
                return redirect(url_for('meets'))

            if buttons.submit_del.data:
                with db.db_session() as session:
                    meet = session.query(Meeting).filter(Meeting.id == buttons.current_meet.data).first()
                    meet.del_user(current_user.id)
                    session.commit()
                return redirect(url_for('meets'))

            if buttons.submit_edit.data:
                return redirect(url_for('profile'))

        with db.db_session() as session:
            query = session.query(Meeting)
            meets_list = paginate(query, page, GAMES_PER_PAGE).all()
            last_page = ceil(session.query(Meeting).count()/GAMES_PER_PAGE)
        return render_template(
            'meets.html', meets_list=meets_list, page_title=title, current_page=page,
            last_page=last_page, buttons=buttons, current_user=current_user)


    return app
