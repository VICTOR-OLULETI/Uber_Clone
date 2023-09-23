from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
import mysql.connector
from flask_login import LoginManager,login_user, logout_user, login_required, current_user
from db import *
from user import * 
from pymongo.errors import DuplicateKeyError
from geopy.geocoders import Nominatim
import os

app = Flask(__name__, static_url_path='/static', static_folder='static' )
#SECRET_KEY = os.environ.get('SECRET_KEY')

app.secret_key = "secret_key"  
# Change this to the production variable SECRET_KEY
#app.secret_key = SECRET_KEY

socketio = SocketIO(app)
# setting up the login manager, a function in flask
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# Global variables used within the application
users = {}
username_driver = None
driver_names_and_distances = None
ride_destination = None 
passenger_name = None
chat_room = None
ready_for_ride_requests = []


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    """function to render the landing page html"""
    return render_template('uber.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    """function to render the home page which is the user's dashboard"""
    return render_template('home.html')

@socketio.on("update_home_page")
def update_home_page():
    global username_driver
    try:
        username = current_user.firstname
        if (get_driver(username)):
            userType = "driver"
            print(f"I am a driver: {username}")
            username_driver = username
            join_room('driver')
            join_room(username_driver)
        else:
            userType = "passenger"
            print("I am a passenger")
            join_room('passenger')
        emit("userType", {'userTypes': userType}, room=userType)
    except AttributeError:
        print("You need to register!!!")
    
@socketio.on("position_location")
def keep_track_location(data):
    latitude = data['latitude']
    longitude = data['longitude']
    created_by = data['created_by']
    #the firstname is also the created_by
    firstname = created_by
    current_location = {
        'latitude': latitude,
        'longitude': longitude,
    }
    try:
        if (get_driver(firstname)):
            save_driver_location(firstname, current_location, created_by)
            print("we have position location working")
        else:
            print("Not a driver")
    except DuplicateKeyError:
        """update the location of the driver"""
        update_driver_location(firstname, current_location)

@socketio.on("ready_for_ride_requests")
def ready_for_ride_request(data):
    """this function helps to access the ready_for_ride_requests variable which stores the list of
    drivers ready for ride requests
    """
    global ready_for_ride_requests
    driver = data['driver_name']
    # adding the drivers to the list
    ready_for_ride_requests.append(driver)
    # making the list unique
    ready_for_ride_requests = list(set(ready_for_ride_requests))
    # printing out to check that the variable is working 
    print("we are listening to ready_for_ride_requests socket now")
    print(f"this is the list of drivers who want ride requests {ready_for_ride_requests}")

@socketio.on("new_ride")
def handle_booked_rides(data):
    # this is the passenger zone
    # we are using the ride destination and the passenger name
    global ride_destination
    global passenger_name
    # checking the socket data content
    print(f"this is the data we from new_ride {data}")
    all_distance = {}
    selected_destination = data['selected_destination']
   
    ride_destination = selected_destination
    latitude = data['latitude']
    longitude = data['longitude']
    created_by = data['created_by']
    #the created_by is also the firstname but to maintain readability
    firstname = created_by 
    
    passenger_name = firstname
    #print(f'this is the new ride for {firstname}')
    #print(f'this is the new destination called {selected_destination}')
    current_location = {
        'latitude': latitude,
        'longitude': longitude,
    }
    #print(f'what are you {current_location}')

    try:
        save_rides(firstname, current_location, selected_destination, created_by)
        """check for available drivers, if yes, set up the watch position and get their location(their location should 
        be watch position and it should be constantly updated on the database),
        get the distance between their location and the passenger's location,
        compute the distance, get the speed they are moving and get the time it would take
        for them to get there and send the passenger a prompt that the driver is on the way"""
        #emit('ride_booked', {"selected_destination": selected_destination}, broadcast=True)
    except DuplicateKeyError:
            message = "ride booked"
            print('THERE IS DUPLICATE ERROR')
            #return redirect(url_for('map'))
    # we check the database for the location of all drivers and calculate the distance between the 
    # current location of passenger and driver. whichever is closet is selected that is if
    # user_id selected is the same as the current_user.firstname
    driver_location = get_all_driver_location()
    current_location = { "latitude": 5.436256106310639,
                "longitude": 8.723190279359194}
  
    if (driver_location):
        for key, value in driver_location.items():
            dist = distance_algorithm(current_location, value)
            all_distance[key] = dist
        # Sorting the dictionary by values of the distance gotten in ascending order and get the smallest
        # distance which is the closet driver
        sorted_items = sorted(all_distance.items(), key=lambda x: x[1])
        print(f"this is the sorted item {sorted_items}")
        global driver_names_and_distances
        driver_names_and_distances = sorted_items
        """we should make it global so that if ride is rejected we will remove the first element and
        and reassign the sorted_items to used_distance_items,
        in the new_ride emit we check if this value is none, which would mean the ride was 
        accepted by the first candidate or else we use the used_distance_items instead and emit"""
        # Select the smallest item (key-value pair)
        smallest_distance_name = sorted_items[0]
        print(f"the smallest distance and name {smallest_distance_name}")
        # Extracting the key and value from the smallest distance
        username, dist = smallest_distance_name
        """creating the room for chatting between only driver and passenger """
        global driver_name
        driver_name = username
        found = False 
        for i in sorted_items:
            if i[0] in (ready_for_ride_requests):
                found = True
                username = i[0]
                driver_name = username
                print("we got accurate data for who is available and distance and ... ")
                emit('ride_booked', {"selected_destination": selected_destination, "passenger_name":firstname, "driver_name": username}, room=username)
                break

        if (not found):
            print("no one is available to pick you. we sincerely apologize for this.")
    else:
        print("OOPS, we have no data for the drivers")
    return redirect(url_for('map'))

@socketio.on("ride_accepted")
def ride_accepted(data):
    # driver zone
    # assigning value for chat_room 
    global chat_room
    global driver_name
    global passenger_name 

    # the global variables should have values from new_ride socket before here
    #driver_name = data['driver_name']
    print(f"This is from listening to ride_accepted {driver_name}")
    
    #passenger_name = data['passenger_name']
    #driver_name = data['driver_name']
    new_room = driver_name + passenger_name
    chat_room = new_room 
    print(f"joining the room {chat_room} from the accept ride socket, driver zone ")
    join_room(new_room) 
    print("The driver is on his way")
    """the driver and passenger will join the same room here identified by the adding of the
    driver and passenger name and this will be used to retrieve message as well order by the 
    timestamp"""
    emit("driver_response", {"driver_name": driver_name}, room='passenger')

@socketio.on('ride_rejected')
def ride_rejected(data):
    #driver_zone
    old_driver = data["driver_name"]
    #old_driver = data['driver_name']
    """we will leave the current room, the driver and passenger, create a new room and join the room"""
    global driver_names_and_distances
    #global username_driver
    global ride_destination
    global passenger_name
    global driver_name 
    global chat_room 
    global ready_for_ride_requests

    print('The Closset driver canceled the ride request')
    print(f"this is the constant driver location {driver_names_and_distances}")
    # since the list is ordered we can do this or just remove the element since we know the name of the driver
    driver_names_and_distances = driver_names_and_distances[1:]
    if (driver_names_and_distances):
        next_smallest_distance_and_name = driver_names_and_distances[0]
        print(f'these are the driver names and distances we have {driver_names_and_distances}')
        print(f"the next smallest distance {next_smallest_distance_and_name}")
        # Extracting the key and value from the smallest distance
        
        username, dist = next_smallest_distance_and_name
        found = False
        for i in driver_names_and_distances:
            if i[0] in (ready_for_ride_requests):
                found = True
                username = i[0]
                driver_name = username
                print("we got accurate data for who is available and distance and ... ")
                new_room = driver_name + passenger_name
                chat_room = new_room
                print(f"joining the room {chat_room} from the reject ride socket, driver zone ")
                join_room(chat_room)
                emit('ride_booked', {"selected_destination": ride_destination, "passenger_name":passenger_name, "driver_name": username}, room=username)
                break

        if (not found):
            print("no one is available to pick you. we sincerely apologize for this.")
        """
        # leave current room whose ride was canceled
        #old_room = old_driver + passenger_name 
        #leave_room(old_room)
        # then, i think the driver never entered any old room, only the passenger
        new_room = driver_name + passenger_name
        chat_room = new_room
        print(f"joining the room {chat_room} from the reject ride socket, driver zone ")
        join_room(chat_room)
        
        emit('join_driver_passenger', {"driver_name": driver_name,
                                        "old_driver": old_driver,
                                    "passenger_name": passenger_name}, room = 'passenger')

        emit('ride_booked', {"selected_destination": ride_destination, "passenger_name":passenger_name, "driver_name": username }, room=username)
        """
    else:
        print("OOPS, we have no data for the drivers")
    return redirect(url_for('map'))


@app.route('/map', methods=['GET', 'POST'])
@login_required
def map():
    print(f'the current user name is {current_user.firstname}')
    try:
        rides = get_ride(current_user.firstname)
        print(f'your ride is {rides}')
        destination = rides.destination
    except:
        flash('Kindly fill the form and click save to use map!', 'error')
        return redirect(url_for("home"))

    current_location = rides.current_location
    latitude = current_location['latitude']
    longitude = current_location['longitude']
    #print(f"your currrent location is {rides['current_location']}")
    def get_place_info(latitude, longitude):
        geolocator = Nominatim(user_agent="myGeocoder")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        
        if location:
            return location.address
        else:
            return "Location not found."

    place_info = get_place_info(latitude, longitude)
    print(f"Place Info: {place_info}")
  
    return render_template('map.html', latitude=latitude, longitude=longitude, start=place_info, destination=destination)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    message = ''
    if request.method == 'POST':
        firstname = request.form.get("firstname")
        print(f'Name is {firstname}')
        password_input = request.form.get("password")
        user = get_user(firstname)
        driver = get_driver(firstname)
        print(f'Driver info is {driver}')
        print(f'User info is {user}')

        if user and user.check_password(password_input):
            login_user(user)
            
            return redirect(url_for('home'))
        elif driver and driver.check_password(password_input):
            login_user(driver)
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'

    return render_template('login.html', message=message)

@app.route("/signup", methods=["GET", "POST"], strict_slashes=False)
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        """The username is also the first name from the html code"""
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = save_user(firstname, lastname, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!" 
    return render_template("user_registration_form.html", message=message)

@app.route("/driversignup", methods=["GET", "POST"], strict_slashes=False)
def driver_signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        """The username is also the first name from the html code"""
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        vehicle_type = request.form.get("vehicle_type")
        available = request.form.get("available")

        try:
            driver = save_driver(firstname, lastname, email, password, vehicle_type, available)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "Driver user already exists!"  
    return render_template("driver_signup.html", message=message)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# API endpoint to receive and store passenger and ride details
@app.route('/book_ride', methods=['GET', 'POST'])
def book_ride():
    if request.method == "POST":
        #passenger_name = data.get('passenger_name')
        selected_ride = request.form['selected_ride']
        selected_destination =request.form['selected_destination']
        estimated_fare = request.form['estimated_fare']

        # Store the data in the database
    return render_template('passenger_home_screen.html')


@app.route('/chat', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def chat():
    global driver_name
    global passenger_name
    global chat_room
    if request.method == 'POST':
        username = request.form.get('firstname')
        try:
            print(f'accessible, this is the driver name from chat function {driver_name}')
            print(f'chat_room {chat_room} is accessible to chat function ')
            messages = get_messages(chat_room)
            """thought: can the messages be identified based on destination"""
            #join_room(chat_room)
            print(f'This is name: {username}')
            if username:
                return render_template('chatbox.html', firstname=username, room=chat_room, messages=messages)
        except:
            flash("No driver has been selected yet, book a ride/get ride request", "success")
            print(f'No driver identified yet!')
            #return redirect(url_for('home'))

    return redirect(url_for('home'))

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(data):
    # passenger zone and driver zone
    username = data["username"]
    print(f"User {username} joined!")
    users[username] = request.sid
    global driver_name
    global passenger_name
    global chat_room
    # we will check if the username gotten is either the passenger name or driver name
    # and then we make them to join the room we will name as chat_room
    # if not print('no access until ride is booked')
    
    if (not chat_room):
        print("no driver identified, you have to book a ride first")
        return (redirect(url_for('home')))
        # we would emit a response and give a prompt/alert at the html side to this effect later
    else:
        #chat_room = driver_name + passenger_name
        print(f'this is you old chat_room: {chat_room}')
    try:
        #the driver has joined the room already from either accept_ride / reject ride socket
        # so we need to only compare for passenger_name but we can leave it like this
        if (username == driver_name) or (username == passenger_name ):
            #chat_room = driver_name + passenger_name
            print(f"this is your new chat_room: {chat_room}")
            join_room(chat_room)
    except:
        print('no access until ride is booked')
            # we would emit a response and give a prompt/alert at the html side to this effect later
    """you could make them join a new room here although it is not necessary as we should be emiting messages
    to the chat_room """
    """
    "" another way is to check the username and verify if it is part of the chat_room component which consist of driver and passenger name ""
    "then you add them to the room "
    global chat_room
    if (chat_room):
        print("I am to enter room: {chat_room} to chat)
        join_room(chat_room)
    """
@socketio.on("new_message")
def handle_new_message(data):
    global chat_room
    message = data["message"] 
    userType = data["usertype"]
    #username = data["username"]
    timestamp = datetime.datetime.now()
    timestamp = str(timestamp)
    print(f'New message: {message}')
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    #save_message(room_type=userType, text=message, sender=data["username"])
    #global chat_room
    #save_message(room_type=chat_room, text=message, sender=data["username"])
    # retreive the chat_room value and save messages into it and emit in to it
    
    join_room(chat_room)
    save_message(room_type=chat_room, text=message, sender=data['username'])
    emit("chat", {"message": message, "username": username, "usertype": userType, "timestamp": timestamp}, room = chat_room)
    #emit("chat", {"message": message, "username": username, "usertype": userType, "timestamp":timestamp}, broadcast=True)


@login_manager.user_loader
def load_user(username):
    user  = get_user(username)
    if not user:
        user = get_driver(username)
    return user
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''