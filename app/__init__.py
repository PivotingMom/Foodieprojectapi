from flask import Flask, jsonify, request, make_response
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import bcrypt
import uuid



# configuration

app = Flask(__name__)
app.testing = True

# enable CORS
CORS(app, resources={ r'/*': { 'origins': '*' } })

from endpoints import client, login, menu_item, order, restaurant 

