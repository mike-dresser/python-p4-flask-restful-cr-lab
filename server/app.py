#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
       all_plants = Plant.query.all() 
       res_body = [plant.to_dict() for plant in all_plants]
       return res_body, 200

    def post(self):
        json_data = request.get_json()
        new_plant = Plant()
        for key, value in json_data.items():
            setattr(new_plant, key, value)
        db.session.add(new_plant)
        db.session.commit()
        return new_plant.to_dict(), 201
  
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
   def get(self, id):
       plant = Plant.query.filter_by(id=id).first()
       return plant.to_dict(), 200

api.add_resource(PlantByID, '/plants/<int:id>')     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
