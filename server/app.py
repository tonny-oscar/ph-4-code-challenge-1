#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# # Define a resource for Hero
# class HeroResource(Resource):
#     def get(self):
#         heroes = Hero.query.all()
#         return [hero.to_dict() for hero in heroes], 200


# # Add the resource to the API
# api.add_resource(HeroResource, '/heroes')


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

# Route to fetch all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

# Route to fetch a hero by ID
@app.route('/heroes/<int:id>/', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict()), 200
    else:
        return {"error": "Hero not found"}, 404


# Run the Flask app on port 5555
if __name__ == '__main__':
    app.run(port=5555, debug=True)
