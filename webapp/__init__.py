from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.database import db, db_session
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.meeting.views import blueprint as meeting_blueprint
from webapp.location.views import blueprint as location_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.methods import get_news

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Для доступа на эта страницу необходимо авторизоваться!'

    app.register_blueprint(user_blueprint)
    app.register_blueprint(meeting_blueprint)
    app.register_blueprint(location_blueprint)
    app.register_blueprint(news_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        with db_session() as session:
            return session.query(User).get(user_id)

    @app.errorhandler(500)
    def server_error():
        title = 'Ошибка получения данных'
        return render_template('server_error.html', page_title=title), 500

    @app.route('/')
    def index():
        title = 'Поиск напарников для настольных игр'
        published_news = get_news()
        return render_template('index.html', page_title=title, list_news=published_news)

    return app
