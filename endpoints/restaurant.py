from app import app
from flask import Flask, jsonify, request
import json
import datetime
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
    query = 'INSERT INTO restaurant (email, name, address, phone_number, bio, banner_url, profile_url, password, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'

    
    email = request_payload.get('email')
    name = request_payload.get('name')
    address = request_payload.get('address')
    phone_number = request_payload.get('phoneNum')
    bio = request_payload.get('bio')
    profile_url = request_payload.get('profileUrl') or 'https://images.pexels.com/photos/3522790/pexels-photo-3522790.jpeg'
    banner_url = request_payload.get('bannerUrl') or 'https://images.pexels.com/photos/566566/pexels-photo-566566.jpeg'
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(request_payload.get('password').encode(), salt)
    city = request_payload.get('city')
    
    
    print([email, name, address, phone_number, bio, banner_url, profile_url, password, city])


    result = run_query(query, [email, name, address, phone_number, bio, banner_url, profile_url, password, city])

    return jsonify('restaurant created', 200)

def get_restaurant_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=10000)
    print(max_token_age)
    
    query = 'SELECT restaurant_Id from restaurant_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None

@app.patch('/api/restaurant')
def update_restaurant():
    data=request.get_json()
    token = request.headers.get('token')
    
    restaurant_Id = get_restaurant_Id(token)
    
    if restaurant_Id:
        #gets all entirs for comparison
        query = 'SELECT * from restaurant WHERE Id =?'
        
        result = run_query(query, ( restaurant_Id,))
        
        print(result)
        

        address = data.get('address') or result[0][3]
        phone_number = data.get('phoneNum') or result[0][4]
        bio = data.get('bio') or result[0][5]
        profile_url = data.get('profileUrl') or 'https://images.pexels.com/photos/3522790/pexels-photo-3522790.jpeg'
        banner_url = data.get('bannerUrl') or 'https://images.pexels.com/photos/566566/pexels-photo-566566.jpeg'
        city = data.get('city') or result[0][9]
    

        print(restaurant_Id)
        
        
        query = 'UPDATE restaurant SET address=?, city=?, bio=?, phone_number=?, profile_url=?,  banner_url=? WHERE Id = ?'
        result = run_query(query, (address, city, bio, phone_number,profile_url, banner_url,  restaurant_Id))
    
        return jsonify('restaurant updated', 200)

    else: 
        return jsonify('no restaurant')