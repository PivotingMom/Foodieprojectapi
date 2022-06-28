from app import app
from flask import Flask, jsonify, request
import json
import datetime
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid

from endpoints.login import get_client_Id
from endpoints import client, restaurant
from endpoints.menu_item import get_restaurant_Id



@app.get('/api/order')
def get_order():
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    
    
    if client_Id:
        
        query= 'SELECT * FROM orders INNER JOIN order_menu_item ON orders.id = order_menu_item.order_id where orders.client_Id=?'

        
        results = run_query(query, (client_Id,))
        
        print(results)
        if results:
            items = []
            output=[]
            orderId=results[0][0]
        
            for result in results:
            
            
                if orderId != result[0]:
                    output.append({
                    'client_Id': result[0],
                    'createdAt': result[1],
                    'is_cancelled': result[5],
                    'is_completed': result[3],
                    'is_comfirmed': result[2],
                    'items': items,
                    'order_id':result[0],
                    'restaurant_id': result[6]
                    })
                    items = []
                items.append(result[8])
    
    restaurant_Id = get_restaurant_Id(token)
    if restaurant_Id:
        

            return jsonify('order completed', 200)
    
    else:
        return jsonify('invalid token', 401)


    
@app.post('/api/order')
def create_order():
    request_payload = request.get_json()
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    
    if client_Id:
        
        query = 'INSERT INTO orders (client_id, restaurant_id) VALUES (?,?)'
        
        restaurantId = request_payload.get('restaurantId')
        items = request_payload.get('items')
    
        orderId = run_query(query, (client_Id, restaurantId))
        query = 'INSERT INTO order_menu_item (menu_item_id, order_id) VALUES (?,?)'
        
        
        for item in items:
            run_query(query, (item, orderId))


        return jsonify('order created', 200)


@app.patch('/api/order')
def update_order():
    request_payload = request.get_json()
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    
    if client_Id:
        orderId = request_payload.get('orderId')
        cancelOrder= request_payload.get('cancelOrder')
    
        query = 'UPDATE orders SET is_cancelled=? WHERE Id = ?'
        
        result = run_query(query, (cancelOrder, orderId)) 
        
        return jsonify('order updated', 200)
    
    restaurant_Id = get_restaurant_Id(token)
    if restaurant_Id:
        orderId = request_payload.get('orderId')
        confirmOrder= request_payload.get('confirmOrder') 
        completeOrder= request_payload.get('completeOrder')
        
        if confirmOrder and completeOrder:
        
            return jsonify('you cannot pass both commands', 422)
        
        if confirmOrder:    
            query = 'UPDATE orders SET is_confirmed=? WHERE Id = ?'
        
            result = run_query(query, (confirmOrder, orderId)) 
        
            return jsonify('order confirmed', 200)
        
        if completeOrder:    
            query = 'UPDATE orders SET is_complete=? WHERE Id = ?'
        
            result = run_query(query, (completeOrder, orderId)) 

            return jsonify('order completed', 200)
    
    else:
        return jsonify('invalid token', 401)