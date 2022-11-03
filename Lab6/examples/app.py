# Using flask to make an api
# import necessary libraries and functions
from flask import Flask, jsonify, request
from pymongo import MongoClient
import datetime
# creating a Flask app
app = Flask(__name__)

client = MongoClient()
db = client['test']

col = db['test_items']

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
          
        data = "hello world"
    item = {'data': data}
    col.insert_one(item)
    return jsonify(item)

# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):

    return jsonify({'data': num**2})

# driver function
if __name__ == '__main__':

    app.run(debug = True)
