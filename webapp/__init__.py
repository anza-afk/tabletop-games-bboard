from crypt import methods
from werkzeug.security import generate_password_hash
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user
from news_parser.test_parser import result_news
from webapp.forms import LoginForm, RegistrationForm
from webapp.users import check_user, add_user
from webapp.models import User


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
                login_user(user)
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
                # return redirect('/')

        return render_template('registration.html', page_title = title, form = registration_form)
    
    return app
