from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # only pass certain fields through JSON to our endpoints
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id.")

    @jwt_required()
    def get(self, name): # accessed with GET method
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        # Check that item is new:
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exists'}, 400

        data = Item.parser.parse_args()
        # data['price'], data['store_id'] = **data
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': "An error occured inserting the item."}, 500 # Internal server error

        return item.json(), 201 # 201 - http code for "created"

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted.'}

    def put(self, name): # can creare new items like POST, but can ALSO modify existing items (e.g. change price in the Body in postman)
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            # data['price'], data['store_id'] = **data
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        # Because the item is uniquelly identified by its id, can save updates to the db as such:
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
