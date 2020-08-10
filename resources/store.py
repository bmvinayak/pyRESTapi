from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.store import StoreModel
from models.item import ItemModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Store Name cannot be blank!"
                        )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "A store with name '{}' does not exist.".format(name)}, 404

    @jwt_required()
    def post(self):
        request_data = Store.parser.parse_args()
        if StoreModel.find_by_name(request_data['name']):
            return {"message": "A store with name '{}' already exists.".format(request_data['name'])}, 400

        store = StoreModel(request_data['name'])

        try:
            store.save_to_db()
        except:
            # internal server error
            return {"message": "An error occured while inserting the store"}, 500

        return store.json(), 201

    @ jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {"message": "Store with name '{}' could not be found.".format(name)}, 400

        items = ItemModel.find_by_store_id(store.id)
        if items:
            return {"message": "There are items in the store '{}'. It cannot be deleted.".format(name)}, 201
        
        store.delete_from_db()
        return {"message": "A store with name '{}' deleted.".format(name)}, 201


class Stores(Resource):
    @ jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
