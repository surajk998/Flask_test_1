# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import jsonify
from models.items import ItemModel


class Item(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument('price',
  type=float,
  required=True,
  help="this field cannot be empty" 
  )
  parser.add_argument('store_id',
  type=int,
  required=True,
  help="this field cannot be empty" 
  )

  @jwt_required()
  def get(self,name):
    item = ItemModel.find_by_name(name)
    if item:
      return item.json()
    return {'message':'Item not found'}, 404

  def post(self,name):
    if ItemModel.find_by_name(name):
      return {'message':f"item {name} already exists"} , 400
    data = Item.parser.parse_args()
    item = ItemModel(name,data['price'], data['store_id'])
    try:
      item.save_to_db()
    except:
      return {'message':"An Error occurred while inserting" }, 500
    return item.json(), 201

  def put(self,name):
    data = Item.parser.parse_args()
    item = ItemModel.find_by_name(name)
    if ItemModel.find_by_name(name):
      item.price = data['price']
    else:
      item = ItemModel(name, **data)
    item.save_to_db()
    return item.json()

  def delete(self, name):
    item = ItemModel.find_by_name(name)
    if item:
      item.delete_from_db()
    return {'message':"Item Deleted"}

  # def delete(self,name):
  #   if ItemModel.find_by_name(name):
  #     connection = sqlite3.connect('data.db')
  #     cursor = connection.cursor()
  #     query = "DELETE FROM items WHERE name=?"
  #     cursor.execute(query,(name,))
  #     connection.commit()
  #     connection.close()
  #     return {"message": "Item Deleted"}
  #   return {'message': 'Item does not exist'}, 400

class ItemList(Resource):
  def get(self):
    return {'Items': list(map(lambda x:x.json(),ItemModel.query.all()))}
    # return {'Items': [ item.json() for item in ItemModel.query.all()]}

    # connection = sqlite3.connect('data.db')
    # cursor = connection.cursor()
    # query = "SELECT * FROM items"
    # result = cursor.execute(query)
    # items = []
    # for row in result:
    #   items.append({'name':row[0],'price':row[1]})
    # connection.close()
    # return {'items': items}

