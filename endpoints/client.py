from app import app
from flask import Flask, jsonify, request
import json
import datetime
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid

from endpoints.login import client_login




@app.get('/api/client')
def get_clients():
    query = 'SELECT * FROM client'
    result = run_query(query)

    return jsonify(result)

@app.post('/api/client')
def create_client():
    request_payload = request.get_json()
    query = 'INSERT INTO client (email, username, password, first_name, last_name, picture_url) VALUES (?,?,?,?,?,?)'

    email = request_payload.get('email')
    username = request_payload.get('username')
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(request_payload.get('password').encode(), salt)
    first_name = request_payload.get('first_name')
    last_name = request_payload.get('last_name')
    picture_url = request_payload.get('picture_Url') or 'https://images.pexels.com/photos/2664216/pexels-photo-2664216.jpeg'
    
    result = run_query(query, (email, username, password, first_name, last_name, picture_url))

    return jsonify('client created', 200)

def get_client_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
    print(max_token_age)
    
    query = 'SELECT client_Id from client_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None
    
@app.patch('/api/client')
def update_client():
    data=request.get_json()
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    if client_Id:
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        picture_url = data.get('picture_Url') 

        print(client_Id)
        
        query = 'UPDATE client SET first_name=?, last_name=?, picture_url=? WHERE Id = ?'
        result = run_query(query, (first_name, last_name, picture_url, client_Id)) 
        
        return jsonify('client updated', 200) 
    
    else: 
        return jsonify('no client')
    
    
@app.delete('/api/client')
def delete_client():
    token = request.headers.get('token')
    client_Id = get_client_Id(token)
    if client_Id:
        """ query = 'DELETE from client_session WHERE client_Id = ?'
        run_query(query, (client_Id,)) """
        
        query = 'DELETE from client WHERE Id = ?'
        run_query(query, (client_Id,))
        
        return jsonify('client deleted', 200) 
    else: 
        return jsonify('no client to delete', 200)
    
    
    #FK on delete/ on update cascade 