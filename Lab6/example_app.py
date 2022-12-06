#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/', methods=['GET'])
def query_records():
    return jsonify({'error': 'data not found'})

@app.route('/', methods=['PUT'])
def update_record():
    return jsonify(record)

@app.route('/', methods=['POST'])
def create_record():
    return jsonify(record)
    
@app.route('/', methods=['DELETE'])
def delte_record():
    return jsonify(record)

app.run(debug=True)
