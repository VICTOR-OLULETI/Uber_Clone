from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit, join_room, leave_room
import mysql.connector
from flask_login import LoginManager,login_user, logout_user, login_required, current_user
from db import *
from user import * 
from pymongo.errors import DuplicateKeyError
from geopy.geocoders import Nominatim

app = Flask(__name__, static_url_path='/static', static_folder='static' )
app.secret_key = "your_secret_key"  # Change this to a secure secret key
socketio = SocketIO(app)
# setting up the login manager, a function in flask
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# Database setup for mysql even though it wasn't used
DATABASE = {
    "user": "username",
    "password": "your password",
    "host": "localhost",
    "database": "Uber"
}
users = {}

def get_db():
    db = mysql.connector.connect(**DATABASE)
    return db


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    """
    selected_destination = request.form.get('selected_destination')
    print(f"this is my selected destination from hoome {selected_destination}")
    """
    #rides = get_ride(current_user.firstname)
    #if (rides) and (not rides.destination):
    #    return redirect(url_for('map'))
    #else:
    #    print(f"I already have a ride destiation")
    return render_template('uber.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def home():
    """
    selected_destination = request.form.get('selected_destination')
    print(f"this is my selected destination from hoome {selected_destination}")
    """
    #rides = get_ride(current_user.firstname)
    #if (rides) and (not rides.destination):
    #    return redirect(url_for('map'))
    #else:
    #    print(f"I already have a ride destiation")
    return render_template('home.html')



@socketio.on("update_home_page")
def update_home_page():
    try:
        username = current_user.firstname
        if (get_driver(username)):
            userType = "driver"
            print(f"I am a driver")
        else:
            userType = "passenger"
            print("I am a passenger")
        emit("userType", {'userTypes': userType}, broadcast=True)
    except AttributeError:
        print("You need to register!!!")
    
@socketio.on("new_ride")
def handle_booked_rides(data):
    current_location = {}
    selected_destination = data['selected_destination']
    latitude = data['latitude']
    longitude = data['longitude']
    created_by = data['created_by']
    firstname = created_by 
    print(f'this is the new ride for {firstname}')
    print(f'this is the new destination called {selected_destination}')
    current_location['latitude'] = latitude
    current_location['longitude'] = longitude
    print(f'what are you {current_location}')
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
    emit('ride_booked', {"selected_destination": selected_destination}, broadcast=True)
    return redirect(url_for('map'))

@socketio.on("ride_accepted")
def ride_accepted():
    #response = data["response"]
    print("The driver is on his way")
    #emit("driver_response", response)


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
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        room = request.form.get('room')
        messages = get_messages(room)

        print(f'This is name: {firstname}')
        if firstname and room:
            return render_template('chatbox.html', firstname=firstname, room=room, messages=messages)
    return redirect(url_for('home'))

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(data):
    username = data["username"]
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(data):
    message = data["message"] 
    userType = data["usertype"]
    #username = data["username"]
    print(f'New message: {message}')
    username = None
    for user in users:
        if users[user] == request.sid:
            username = user
    save_message(room_type=userType, text=message, sender=data["username"])
    emit("chat", {"message": message, "username": username, "usertype": userType}, broadcast=True)


@login_manager.user_loader
def load_user(username):
    data  = get_user(username)
    if data:
        return data
    else:
        return get_driver(username)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
'''