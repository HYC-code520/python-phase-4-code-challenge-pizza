#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


#Helper function
def find_restaurant_by_id(id):
    return Restaurant.query.where(Restaurant.id ==id).first()  #### mistake was Restaurant.id not Restaurants.id

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

#GET /restaurants
@app.get('/restaurants')
def all_restaurants():
    restaurants = Restaurant.query.all()
    restaurant_dicts = [restaurant.to_dict( rules=('-restaurant_pizzas',) ) for restaurant in restaurants]
    return restaurant_dicts, 200


#GET /restaurants/int:id
@app.get('/restaurants/<int:id>')
def get_restaurant(id):
    restaurant = find_restaurant_by_id(id)
    if restaurant:
        return restaurant.to_dict(), 200
    else:
        return { "error": "Restaurant not found" }, 404


#DELETE /restaurants/int:id
@app.delete('/restaurants/<int:id>')
def delete_restaurant(id):
    restaurant = find_restaurant_by_id(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return "", 204
    else:
        return { "error": "Restaurant not found" }, 404



#GET /pizzas
@app.get('/pizzas')
def all_pizzas():
    pizzas = Pizza.query.all()
    pizza_dicts = [ pizza.to_dict( rules=('-restaurant_pizzas',) ) for pizza in pizzas ]
    return pizza_dicts, 200

#POST /restaurant_pizzas
@app.post('/restaurant_pizzas')
def post_restaurant_pizzas():
    try:
        body = request.json
        new_restaurant_pizza = RestaurantPizza(
            price=body.get('price'),
            pizza_id=body.get('pizza_id'),
            restaurant_id=body.get('restaurant_id')
        )
        db.session.add(new_restaurant_pizza)
        db.session.commit()
        return new_restaurant_pizza.to_dict(), 201
    except ValueError:
        return { 'errors': ["validation errors"] }, 400





if __name__ == "__main__":
    app.run(port=5555, debug=True)
