from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from user import *
import datetime
import math



#MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient("mongodb+srv://test:test@chatapp.sqimylr.mongodb.net/") 
# changing this to the production variable MONGODB_URI will now be
#client = MongoClient(MONGODB_URI)

chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
drivers_collection = chat_db.get_collection("drivers")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")
messages_collection = chat_db.get_collection("messages")
rides_collection = chat_db.get_collection("rides")
drivers_location_collection = chat_db.get_collection("drivers_location")

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

def save_driver_location(firstname, current_location, created_by):
    drivers_location_collection.insert_one({'_id': firstname, 'current_location': current_location,
                                        'created_by': created_by})

def update_driver_location(firstname, current_location):
    myquery = { "_id": firstname }
    newvalues = { "$set": { "current_location": current_location} }
    drivers_location_collection.update_one(myquery, newvalues)

def get_user(firstname):
    user_data = users_collection.find_one({'_id': firstname})
    return User(user_data['_id'], user_data['lastname'], user_data['email'], user_data['password']) if user_data else None

def get_driver(firstname):
    driver_data = drivers_collection.find_one({'_id': firstname})
    return Driver(driver_data['_id'], driver_data['lastname'], driver_data['email'], driver_data['password'], driver_data['vehicle_type'], driver_data['available']) if driver_data else None

def distance_algorithm(first_location, second_location):
    """computing distance using longitude and latitude"""
    lon1 = first_location['longitude']
    print(f"longitude is {lon1}")
    lat1 = first_location['latitude']
    print(f"latitude is {lat1}")
    lon2 = second_location['longitude']
    lat2 = second_location['latitude']
    """After computation of algorithm we return the value but for now 
    we return true"""
    print(f"lon1 {lon1}")
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Radius of the Earth (mean value) in kilometers
    radius = 6371.0

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

def get_all_driver_location():
    """get all current_location and the firstname in a dictionary for all records"""
    current_location = drivers_location_collection.find()
    driver_location = {}
    all_distance = {}
    for loc in current_location:
        name = loc['_id']
        location = loc['current_location']
        driver_location[name] = location
    print(f"These are the data for driver location {driver_location}")
    return driver_location
    """
    passenger_locations = {}
    passenger_locations['latitude'] = 'latitude'
    passenger_locations['longitude'] = 'longitude'
    for key, value in driver_location.items():
        dist = distance_algorithm(passenger_locations, value)
        all_distance[key] = dist
    sorted_items = sorted(all_distance.items(), key=lambda x: x[1])
    print(all_distance)
    print(sorted_items)
    smallest_distance = sorted_items[0]
    print(f"this is the smallest distance {smallest_distance}")
    username, dist = smallest_distance
    print(f"the username is {username}")
    return all_distance
    #return current_location['current_location'] if current_location else None 
    """

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



#get_all_driver_location()
