
from flask import Flask, render_template
from news_parser.test_parser import result_news

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def index():
        title = 'Поиск напарников для настольных игр'
        return render_template('index.html', page_title=title, list_news=result_news)
    return app
    
    