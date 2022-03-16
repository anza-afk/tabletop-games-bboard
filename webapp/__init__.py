from cmath import pi
import imp
from werkzeug.security import generate_password_hash
from flask import Flask, redirect, render_template, request
from news_parser.test_parser import result_news
from webapp.forms import LoginForm, RegistrationForm
from webapp.users import check_user, add_user
from webapp.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    @app.route('/')
    def index():
        title = 'Поиск напарников для настольных игр'
        return render_template('index.html', page_title=title, list_news=result_news)
    
    @app.route('/login')
    def login():
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', page_title = title, form = login_form)

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
