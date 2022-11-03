from pymongo import MongoClient

# Creates the db client (i.e. where is the db hosted)
client = MongoClient()

#Sets the name of the database
db = client['lab6_db']

#Create a collection to store sensor data
collection = db["accelerometer_data"]


