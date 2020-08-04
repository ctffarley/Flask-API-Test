from flask import Flask, request
from flask_restx import Resource, Api, fields
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

db_string = 'postgresql://postgres:pass@127.0.0.1:5432/restaurant'
db = create_engine(db_string)  
base = declarative_base()

item = api.model('Food', {
    'id': fields.Integer(description = 'The food id'),
    'name': fields.String(required=True, description = 'The food name'),
    'price': fields.Integer(required=True, description = 'The food price')
})

ns = api.namespace('menu', description='menu CRUD operations')

# class Food:
#     def __init__(self, name, price, id):
#         self.name = name
#         self.price = price
#         self.id = id

#     def update_price(self, price):
#         self.price = price

# class Menu:
#     def __init__(self):
#         self.items = []
#         self.count = 0

#     def list_items(self):
#         return self.items

#     def add_item(self, name, price):
#         self.items.append(Food(name, price, self.count))
#         self.count += 1

#     def remove_item(self, item):
#         self.items.remove(item)

#     def update_price(self, id, price):
#         for i in self.items:
#             if i.id == id:
#                 i.update_price(price)

#     def get_item(self, id):
#         for i in self.items:
#             if i.id == id:
#                 return i


# menu = Menu()

# menu.add_item('Burger', 10)

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
    app.run()