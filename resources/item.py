from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Item Name cannot be blank!"
                        )    
    parser.add_argument('price',
                        type=float, 
                        required=True, 
                        help="Item price cannot be blank!"    
    )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store_id cannot be blank!"
                        )

    @jwt_required()
    def get(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if item:
            return item.json()
        return {"message": "An item with id '{}' does not exist.".format(item_id)}, 404

    @jwt_required()
    def post(self):
        request_data = Item.parser.parse_args()
        store = StoreModel.find_by_id(request_data['store_id'])
        
        if store is None:
            return {"message": "Store with id '{}' does not exist.".format(request_data['store_id'])}, 400
        
        if ItemModel.find_by_name(request_data['name'], request_data['store_id']):
            return {"message": "An item with name '{}' already exists in the store '{}'.".format(request_data['name'], request_data['store_id'])}, 400
        
        item = ItemModel(**request_data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting the item"}, 500 # internal server error

        return item.json(), 201

    @jwt_required()
    def put(self):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(
            request_data['name'], request_data['store_id'])

        if item is None:
            item = ItemModel(**request_data)
        else:
            item.price = request_data['price']

        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, item_id):
        item = ItemModel.find_by_id(item_id)
        if item is None:
            return {"message": "Item with id '{}' could not be found.".format(item_id)}, 400
        
        item.delete_from_db()
        return {"message": "An item with id '{}' deleted.".format(item_id)}, 201


class Items(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
