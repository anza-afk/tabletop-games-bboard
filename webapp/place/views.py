from flask import Blueprint, request, jsonify
from webapp.database import db_session
from sqlalchemy.orm import load_only
from webapp.place.models import City


blueprint = Blueprint('place', __name__, url_prefix='/places')

@blueprint.route('/_autocomplete_city', methods=['GET'])
def autocomplete_city():
    with db_session() as session:
        search = request.args.get('q')
        print(search)
        if not search:
            search = []
        city_db = session.query(City).options(load_only('name')).filter(City.name.ilike(f'%{search}%')).limit(5)
        cities_names = [(city.id, city.name) for city in city_db]
        return jsonify(cities_names)
