from datetime import datetime, timedelta
from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import datetime
import bcrypt
import uuid
from endpoints import client, restaurant




@app.post('/api/client_login')
def client_login():
    request_payload = request.get_json()
    query = 'SELECT * FROM client WHERE email=?'

    email = request_payload.get('email')
    password = request_payload.get('password')

    
    result =run_query(query, [email])

    print(result)
    
    if bcrypt.checkpw(password.encode(), result[0][3].encode()):

        token=str(uuid.uuid4())
        run_query( 'INSERT INTO client_session (token, client_Id) VALUES (?,?)', [token, result[0][0]])
        
        
        return jsonify({'clientId':result[0][0],'token':token}), 200
    else:
        return jsonify(result, 401)


def get_client_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
    print(max_token_age)
    
    query = 'SELECT client_Id from client_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None
    
@app.delete('/api/client_login')
def client_login_delete():
    token = request.headers.get('token')
    client_Id = get_client_Id(token)
    if client_Id:
        query = 'DELETE from client_session WHERE client_Id = ?'
        run_query(query, (client_Id,))
        
        #query = 'DELETE from client_session WHERE token =?'
        #run_query(query, (token,)))
        
        return jsonify('token deleted', 204) 
    else: 
        return jsonify('no token to delete', 401)
    

@app.post('/api/restaurant_login')
def restaurant_login():
    request_payload = request.get_json()
    query = 'SELECT * FROM restaurant WHERE email=?'

    email = request_payload.get('email')
    password = request_payload.get('password')

    
    result =run_query(query, [email])

    print(result)
    
    if bcrypt.checkpw(password.encode(), result[0][8].encode()):

        token=str(uuid.uuid4())
        run_query( 'INSERT INTO restaurant_session (token, restaurant_Id) VALUES (?,?)', [token, result[0][0]])

        
        return jsonify({'restaurantId':result[0][0], 'token':token}), 200
    else:
        return jsonify(result, 401)


def get_restaurant_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=120)
    print(max_token_age)
    
    query = 'SELECT restaurant_Id from restaurant_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None

@app.delete('/api/restaurant_login')
def restaurant_login_delete():
    token = request.headers.get('token')
    
    restaurant_Id = get_restaurant_Id(token)
    if restaurant_Id:
        query = 'DELETE from restaurant_session WHERE restaurant_Id = ?'
        run_query(query, (restaurant_Id,))
        
        
        
        return jsonify('token deleted', 204) 
    else: 
        return jsonify('no token to delete', 401)
    
