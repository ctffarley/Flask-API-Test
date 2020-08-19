from flask import Flask, request
from flask_restx import Resource, Api, fields
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)

CORS(app)

db_user = os.environ['POSTGRES_USER']
db_pass = os.environ['POSTGRES_PASSWORD']
db_ip = os.environ['POSTGRES_IP']
db_port = os.environ['POSTGRES_PORT']
db_name = os.environ['POSTGRES_DATABASE']

db_string = f'postgresql://{db_user}:{db_pass}@{db_ip}:{db_port}/{db_name}'
db = create_engine(db_string)  
base = declarative_base()

item = api.model('Food', {
    'id': fields.Integer(description = 'The food id'),
    'name': fields.String(required=True, description = 'The food name'),
    'price': fields.Integer(required=True, description = 'The food price')
})

ns = api.namespace('menu', description='menu CRUD operations')

class Food(base):
    # table for the food be stored in
    __tablename__ = 'menuv2'

    # columns for the table, id autoincrements
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)


# boilerplate initialization for SQLAlchemy
Session = sessionmaker(db)  
session = Session()

base.metadata.create_all(db)

# root page that returns the full contents of the menu
@ns.route('/')
class MenuPage(Resource):
    @ns.marshal_list_with(item)
    def get(self):
        # get all entries from table
        return session.query(Food).all()

# route allows you to delete an item based on id
@ns.route('/delete/<int:id>')
class DeleteItem(Resource):
    def delete(self, id):
        # query based on ID then remove that object
        session.query(Food).filter(Food.id == id).delete()

# This route supports post and put operations to create and update menu items,
# respectively
@ns.route('/item')
class MenuItem(Resource):
    @api.doc(params={'name': 'name of the food', 'price': 'price of the food'})
    def post(self):
        # get parameters from request
        name = request.args['name']
        price = request.args['price']

        # create temporary item
        temp = Food(name=name, price=price)

        # add item to session then commit to database
        session.add(temp)
        session.commit()

    @api.doc(params={'id': 'id of the food item', 'price': 'price of the food'})
    def put(self):
        # get parameters from request
        id = request.args['id']
        price = request.args['price']

        # query the db by id
        target = session.query(Food).filter(Food.id == id).first()

        # change the item's price, then commit to database
        target.price = price
        session.commit()

if __name__ == '__main__':
    app.run(debug=True)