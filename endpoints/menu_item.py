from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid





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

@app.delete('/api/menu_item/<id>')
def delete_menu_item():
    menu_id = request.view_args['id']
    query = 'DELETE FROM menu_item WHERE Id = ?'
    result = run_query(query, (menu_id))
    
    return jsonify('menu item deleted', 200)

@app.patch('/api/menu_item/<id>')
def update_menu_item():
    menu_item_id = request.view_args['id']
    query = 'UPDATE menu_item WHERE Id = ?'
    result = run_query(query, (menu_item_id))
    
    return jsonify('menu item updated', 200)