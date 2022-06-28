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





@app.get('/api/menu')
def get_menu_item():
    restaurantId = request.args.get('restaurantId')
    menuId = request.args.get('menuId')
    
    if restaurantId:
        query = 'SELECT * FROM menu_item WHERE restaurant_Id =?'
        
        
        result = run_query(query, (restaurantId,))
    elif menuId:
        query = 'SELECT * FROM menu_item WHERE Id =?'
        
        
        result = run_query(query, (menuId,))
    else:
        
        query = 'SELECT * FROM menu_item'
        
        result = run_query(query)

        print(result)
        
    formated_result = list(map(lambda x: 
        {'name': x[1],
        'description': x[2],
        'price':x[3],
        'image_url': x[4],
        'restaurant_Id': x[5]

    }, result))
    return jsonify(formated_result)


def get_restaurant_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=10000)
    print(max_token_age)
    
    query = 'SELECT restaurant_Id from restaurant_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None

@app.post('/api/menu')
def create_menu_item():
    request_payload = request.get_json()
    token = request.headers.get('token')
    
    restaurant_Id = get_restaurant_Id(token)
    
    if restaurant_Id:
        
        query = 'INSERT INTO menu_item (name, description, price, image_url, restaurant_Id) VALUES (?,?,?,?,?)'

        name = request_payload.get('name')
        description = request_payload.get('description')
        price = request_payload.get('price')
        image_url = request_payload.get('picture_Url') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    
        result = run_query(query, (name, description, price, image_url, restaurant_Id))

        return jsonify('menu item added', 200)



@app.patch('/api/menu')
def update_menu():
    data=request.get_json()
    token = request.headers.get('token')
    
    restaurant_Id = get_restaurant_Id(token)
    
    if restaurant_Id:
        
        query = 'SELECT * from menu_item WHERE restaurant_Id =? AND Id =?'
        
        menuId = data.get('menuId')
        
        result = run_query(query, ( restaurant_Id, menuId ))
        
        print(result)
        
        if result:
        
            
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            image_url = data.get('picture_Url') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
            menuId = data.get('menuId')
        
        
            query = 'UPDATE menu_item SET name=?, description=?, price=?,  image_url=?  WHERE Id = ?'
            result = run_query(query, (name, description, price, image_url,  menuId))
    
            return jsonify('menu_item updated', 200)
        else:
            return jsonify('invalid token', 401)
        

    else: 
        return jsonify('no menu')
    
@app.delete('/api/menu')
def delete_menu_item():
    data=request.get_json()
    token = request.headers.get('token')
    
    restaurant_Id = get_restaurant_Id(token)
    
    if restaurant_Id:
        
        query = 'SELECT * from menu_item WHERE restaurant_Id =? AND Id =?'
        
        menuId = data.get('menuId')
        
        result = run_query(query, ( restaurant_Id, menuId ))
        
        print(result)
        
        if result:
            
            query = 'DELETE FROM menu_item WHERE Id = ?'
            result = run_query(query, (menuId,))
    
            return jsonify('menu item deleted', 204)
        
            
        else:
            return jsonify('can not find the menu', 422)
    
    else:
        return jsonify('invalid token', 401)
    



