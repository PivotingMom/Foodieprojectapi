from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid 



@app.get('/api/restaurant')
def get_restaurants():
    query = 'SELECT *, restaurant.name AS restaurant_name, city.name AS city_name FROM restaurant INNER JOIN city ON restaurant.city = city.id'
    result = run_query(query)

    formated_result = list(map(lambda x: {
        'address': x['address'],
        'bannerUrl': x['banner_url'],
        'bio': x['bio'],
        'city': x['city_name'],
        'email': x['email'],
        'name': x['restaurant_name'],
        'phoneNum': x['phone_number'],
        'profileUrl': x['profile_url'],
        'restaurantId': x['id']

    }, result))
    return jsonify(formated_result)


@app.post('/api/restaurant')
def create_restaurant():
    request_payload = request.get_json()
    query = 'INSERT INTO restaurant (email, name, address, phone_number, bio, password, city, banner_url, profile_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

    name = request_payload.get('name')
    address = request_payload.get('address')
    banner_url = request_payload.get('bannerUrl') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    profile_url = request_payload.get('profileUrl') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    bio = request_payload.get('bio')
    city = request_payload.get('city')
    email = request_payload.get('email')
    phone_number = request_payload.get('phoneNum')
    password = request_payload.get('password')


    result = run_query(query, (email, name, address, phone_number, bio, password, city, banner_url, profile_url))

    return jsonify('client created', 200)



@app.patch('/api/restaurant')
def update_restaurant():
    restaurant_id = request.view_args['id']
    query = 'UPDATE restaurant WHERE Id = ?'
    result = run_query(query, (restaurant_id))
    
    return jsonify('restaurant updated', 200)
