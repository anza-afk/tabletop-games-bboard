from flask import Blueprint, render_template, request
from webapp.news.models import News
from webapp.database import db_session

blueprint = Blueprint('news', __name__, url_prefix='/news')


@blueprint.route('/news', methods=['GET'])
@blueprint.route('/news/<int:id>', methods=['GET'])
def news():
    with db_session() as session:
        news_id = request.args['id']
        news_data = session.query(News).filter(News.id == news_id).first()
        print(news_data)
    return render_template('news.html', news_data=news_data)
