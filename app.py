from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import datetime


from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, Stores

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'abcxyz'
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(minutes=30)
api = Api(app)

#/auth
jwt = JWT(app, authenticate, identity) 

# http://127.0.0.1/store/store1
api.add_resource(Store, '/store', '/store/<string:name>')  

# http://127.0.0.1/stores
api.add_resource(Stores, '/stores')

# http://127.0.0.1/item http://127.0.0.1/item/1
api.add_resource(Item, '/item', '/item/<int:item_id>')

# http://127.0.0.1/items
api.add_resource(Items, '/items') 

# http://127.0.0.1/register
api.add_resource(UserRegister, '/register') 

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
