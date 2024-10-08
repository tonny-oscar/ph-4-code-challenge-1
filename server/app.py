#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os
# from flask_cors import CORS


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

# CORS(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# Route to fetch all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200

# Route to fetch a hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict()), 200
    else:
        return {"error": "Hero not found"}, 404

# Route to fetch a power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict()), 200
    else:
        return {"error": "Power not found"}, 404

# Route to update by ID
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return {"error": "Power not found"}, 404

    data = request.get_json()
    description = data.get('description', None)

    if description:
        power.description = description
        db.session.commit()
        return jsonify(power.to_dict()), 200
    else:
        return {"error": "Invalid data"}, 400

# Route to post
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    #new_super_hero = hero_power(first_name=data.get('first_name'),last_name=data.get('last_name'), grade=data.get('grade'))
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if not hero_id or not power_id or not strength:
        return {"error": "Missing data"}, 420

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return {"error": "Hero or Power not found"}, 404

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.to_dict()), 201

# Run the Flask app on port 5555
if __name__ == '__main__':
    app.run(port=5555, debug=True)
