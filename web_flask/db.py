from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import *
import datetime

client = MongoClient("mongodb+srv://test:test@chatapp.sqimylr.mongodb.net/")

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
drivers_collection = chat_db.get_collection("drivers")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")
messages_collection = chat_db.get_collection("messages")
rides_collection = chat_db.get_collection("rides")

def save_user(firstname, lastname, email, password):
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': firstname, 'lastname': lastname, 'email': email, 'password': password_hash})

def save_driver(firstname, lastname, email, password, vehicle_type, available):
    password_hash = generate_password_hash(password)
    drivers_collection.insert_one({'_id': firstname, 'lastname': lastname, 'email': email, 'password': password_hash, 'vehicle_type': vehicle_type, 'available': available})

def save_rides(firstname, current_location, selected_destination, created_by):
    rides_collection.insert_one({'_id': firstname, 'current_location': current_location,
                                'selected_destination': selected_destination, 
                                'created_by': created_by})

def get_user(firstname):
    user_data = users_collection.find_one({'_id': firstname})
    return User(user_data['_id'], user_data['lastname'], user_data['email'], user_data['password']) if user_data else None

def get_driver(firstname):
    driver_data = drivers_collection.find_one({'_id': firstname})
    return Driver(driver_data['_id'], driver_data['lastname'], driver_data['email'], driver_data['password'], driver_data['vehicle_type'], driver_data['available']) if driver_data else None

def get_ride(firstname):
    ride_data = rides_collection.find_one({'_id': firstname})
    return Ride(ride_data['_id'], ride_data['current_location'], ride_data['selected_destination'], ride_data['created_by']) if ride_data else None

def update_ride(firstname, new_destination):
    myquery = { "_id": firstname }
    newvalues = { "$set": { "selected_destination": new_destination} }
    rides_collection.update_one(myquery, newvalues)


def save_room(room_name, created_by, usernames):
    room_id = rooms_collection.insert_one({'room_name': room_name, 'created_by': created_by, 'created_at': datetime.datetime.now()}).inserted_id
    add_room_member()

def update_room(room_id, room_name):
    pass

def get_room(room_id):
    pass

def add_room_member(room_id, room_name, username, added_by, is_admin=False):
    pass

def add_room_members(room_id, room_name, usernames, added_by):
    pass

def remove_room_members(room_id, usernames):
    pass

def get_room_members(room_id):
    pass

def get_rooms_for_user(username):
    pass

def is_room_member(room_id, username):
    pass

def save_message(room_type, text, sender):
    messages_collection.insert_one({'room_type':room_type, 'text': text, 'sender': sender, 'created_at': datetime.datetime.now()})

def get_messages(room_type):
    return list(messages_collection.find({'room_type': room_type})) 