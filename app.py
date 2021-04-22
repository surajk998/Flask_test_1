import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resources.user import UserRegister
from security import authenticate,identity
from resources.items import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # JWT creates endpoint name /auth

api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:5000/item/Name
api.add_resource(ItemList, '/items') #http://127.0.0.1:5000/items
api.add_resource(StoreList,'/stores')
api.add_resource(UserRegister,'/register')

if __name__=="__main__":
  from db import db
  db.init_app(app)
  app.run(port = 5000, debug = True) #default value is 5000



# app.config['JWT_AUTH_URL_RULE'] = '/login'
# app.config['JWT_EXPIRATION_DELTA'] =  timedelta(seconds=1800)
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# @jwt.error_handler
# def customized_error_handler(error):
#  return jsonify({
#  'message': error.description,
#  'code': error.status_code
#  }), error.status_code
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#  return jsonify({
#  'access_token': access_token.decode('utf-8'),
#  'user_id': identity.id
#  })
