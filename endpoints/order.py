from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid


@app.get('/api/orders')
def get_order():
    query = 'SELECT * FROM orders'
    result = run_query(query)

    return jsonify(result)

@app.post('/api/order')
def create_order():
    request_payload = request.get_json()
    query = 'INSERT INTO orders (is_confirmed, is_completed, is_cancelled) VALUES (?,?,?)'

    is_confirmed = request_payload.get('is_confirmed')
    is_completed = request_payload.get('is_completed')
    is_cancelled = request_payload.get('is_cancelled')
    
    result = run_query(query, (is_confirmed, is_completed, is_cancelled))

    return jsonify('client created', 200)


@app.patch('/api/client/<id>')
def update_order():
    order_id = request.view_args['id']
    query = 'UPDATE orders WHERE Id = ?'
    result = run_query(query, (order_id))
    
    return jsonify('order updated', 200)