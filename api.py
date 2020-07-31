from flask import Flask, request
from flask_restx import Resource, Api, fields
from sqlalchemy import create_engine

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True
# engine = create_engine('postgresql')

item = api.model('Food', {
    'name': fields.String(required=True, description = 'The food name'),
    'price': fields.Integer(required=True, description = 'The food price')
})

ns = api.namespace('menu', description='menu CRUD operations')

class Food(object):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def update_price(self, price):
        self.price = price

class Menu(object):
    def __init__(self):
        self.items = []

    def list_items(self):
        return self.items

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def update_price(self, item, price):
        for i in self.items:
            if i.name == item:
                i.update_price(price)

    def get_item(self, name):
        for i in self.items:
            if i.name == name:
                return i

menu = Menu()

menu.add_item(Food('Burger', 10))

@ns.route('/')
class MenuPage(Resource):
    @ns.marshal_list_with(item)
    def get(self):
        return menu.items

@ns.route('/delete/<string:name>')
class DeleteItem(Resource):
    def delete(self, name):
        menu.remove_item(name)

@ns.route('/item')
class MenuItem(Resource):
    @api.doc(params={'name': 'name of the food', 'price': 'price of the food'})
    def post(self):
        name = request.args['name']
        price = request.args['price']
        menu.add_item(Food(name, price))

    @api.doc(params={'name': 'name of the food', 'price': 'price of the food'})
    def put(self):
        name = request.args['name']
        price = request.args['price']
        menu.update_price(menu.get_item(name), price)

if __name__ == '__main__':
    app.run()