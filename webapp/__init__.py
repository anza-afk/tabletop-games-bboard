from werkzeug.security import generate_password_hash
from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from news_parser.test_parser import result_news
from webapp.forms import LoginForm, RegistrationForm, ProfileForm
from webapp.users import check_user, add_user, add_profile, join_profile, add_profile, update_profile
from webapp.models import User, User_profile

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


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
        return render_template('login.html', page_title = title, form = login_form)

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
        title = 'Регистрация'
        registration_form = RegistrationForm()
      
        if registration_form.validate_on_submit():
            if not check_user(registration_form['email'].data):
                hash_pass = generate_password_hash(registration_form['password'].data)
                new_user = User(
                    username=registration_form['username'].data,
                    password=hash_pass,
                    email=registration_form['email'].data,
                    role='1'
                    )
                add_user(new_user)
                return redirect('/login')

        return render_template('registration.html', page_title = title, form = registration_form)
    
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
            return redirect(url_for('index'))
        new_profile = User_profile(
            owner_id=current_user.id,
            name=form['name'].data,
            surname=form['name'].data,
            country=form['country'].data,
            city=form['city'].data,
            favorite_games=form['favorite_games'].data,
            desired_games=form['desired_games'].data,
            about_user=form['about_user'].data
        )
        
            #  email_for_user = User()
        add_profile(new_profile)
        flash('Успех!')
        return redirect(url_for('index'))

    
    return app
