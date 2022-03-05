
from flask import Flask, render_template
from test_parser import result_news

app = Flask(__name__)

@app.route('/')
def index():
    title = 'Поиск напарников для настольных игр'
    return render_template('index.html', page_title=title, list_news=result_news)

if __name__ == "__main__":
    app.run(debug=True)