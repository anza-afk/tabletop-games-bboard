from flask import Blueprint, render_template, request
from webapp.methods import get_news

blueprint = Blueprint('news', __name__, url_prefix='/news')


@blueprint.route('/news', methods=['GET'])
@blueprint.route('/news/<int:id>', methods=['GET'])
def news():
    news_id = request.args['id']
    print(news_id)
    news_data = list(filter(lambda n: n['id'] == news_id, get_news()))[0]
    return render_template('news.html', news_data=news_data)
