from app import app
from flask import Flask, jsonify, request
import json
import datetime
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid

from endpoints.login import client_login, restaurant_login





@app.get('/api/menu_item')
def get_menu_item():
    query = 'SELECT * FROM menu_item'
    result = run_query(query)

    return jsonify(result)

@app.post('/api/menu_item')
def create_menu_item():
    request_payload = request.get_json()
    query = 'INSERT INTO menu_item (name, description, price, image_url) VALUES (?,?,?,?)'

    name = request_payload.get('name')
    description = request_payload.get('description')
    price = request_payload.get('price')
    image_url = request_payload.get('picture_Url') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    
    result = run_query(query, (name, description, price, image_url))

    return jsonify('menu item added', 200)

@app.delete('/api/menu_item')
def delete_menu_item():
    menu_id = request.view_args['id']
    query = 'DELETE FROM menu_item WHERE Id = ?'
    result = run_query(query, (menu_id))
    
    return jsonify('menu item deleted', 200)


def get_restaurant_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=120)
    print(max_token_age)
    
    query = 'SELECT restaurant_Id from restaurant_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None


@app.patch('/api/menu_item')
def update_menu_item():
    data=request.get_json()
    token = request.headers.get('token')
    
    restaurant_Id = get_restaurant_Id(token)
    
    if restaurant_Id:
        
        query = 'SELECT restaurant_Id from menu_item WHERE Id =?'
        
        menu_item_Id = data.get('menu_item_id')
        result = run_query(query, ( menu_item_Id,))
        
        if menu_item_Id:restaurant_Id
        
        print(result)

        
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        image_url = data.get('picture_Url') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
        menu_item_Id = data.get('menu_item_id')
        
        
        query = 'UPDATE menu_item SET name=?, description=?, price=?,  image_url=?,  WHERE Id = ?'
        result = run_query(query, (name, description, price, image_url,  menu_item_Id))
    
        return jsonify('menu_item updated', 200)

    else: 
        return jsonify('no menu')


