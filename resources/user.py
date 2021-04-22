import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
  parser =  reqparse.RequestParser()
  parser.add_argument('username', type=str, required=True, help="Username can't be empty")
  parser.add_argument('password', type=str, required=True, help="Password cannot be empty")

  def post(self):
    data = UserRegister.parser.parse_args() 
    if UserModel.find_by_username(data['username']):
      return {'message':'User already exists'}, 400
    # connection = sqlite3.connect('data.db')
    # cursor = connection.cursor()
    # query = "INSERT INTO users VALUES(NULL, ?, ?)"
    # cursor.execute(query, (data['username'],data['password']))
    # connection.commit()
    # connection.close()
    
    user = UserModel(**data)
    user.save_to_db()

    return {'message':'User registered'}, 201

  # @jwt_required()
  # def get(self): # view all users
  #   user = current_identity # gives current user
  #   # then implement admin auth method