import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister
from security import authenticate,identity
from resources.items import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('postgresql://jksralrgzbgkqv:22d21686dbcc42555744d39189f917994303f9b3cf1744911a38ba9dd8fe5c4c@ec2-176-34-222-188.eu-west-1.compute.amazonaws.com:5432/d1a0ov6v0ab3rd','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'suri'
api = Api(app)

jwt = JWT(app, authenticate, identity) 

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items') 
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__=="__main__":
  from db import db
  db.init_app(app)
  app.run(port = 5000, debug = True) #default value is 5000
