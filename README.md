The uber.html file is the Landing page which is the replica of the original uber website page.
I would be updating this README file with the work through of the web application.
kindly bear with me.

AUTHOR: OLULETI VICTOR. gmail: oluletiv@gmail.com
Thanks

## GOAL
The goal of the project is to implement a simplified version of uber web application
we went through
# Authentication
# Communication
# Routing 

## Techonology Used
# python
    INSTALLATION
    sudo apt-get update
    sudo apt install python3

    LIBRARIES
    import json, threading, time, os

# flask(UI)
    INSTALLATION
    pip3 install Flask

    LIBRARIES
    from flask import Flask, render_template, request, redirect, url_for, flash
    from flask_socketio import SocketIO, emit, join_room, leave_room
    from flask_login import LoginManager,login_user, logout_user, login_required, current_user

# Mongodb (database)
    INSTALLATION
    sudo apt install -y mongodb
    pip3 install pymongo


    LIBRARIES
    import pymongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    from pymongo.errors import DuplicateKeyError

# Geopy
    pip3 install geopy

    LIBRARIES
    from geopy.geocoders import Nominatim


MODULES IN OUR APPLICATION
Flask Server
Authentication

## Database
chat_db = client.get_database("ChatDB")
users_collection = chat_db.get_collection("users")
drivers_collection = chat_db.get_collection("drivers")
rooms_collection = chat_db.get_collection("rooms")
room_members_collection = chat_db.get_collection("room_members")
messages_collection = chat_db.get_collection("messages")
rides_collection = chat_db.get_collection("rides")
drivers_location_collection = chat_db.get_collection("drivers_location")


## Using flask
1. Register user
2. Login user
3. Book rides
4. Get ride requests
3. Send Messages
4. Storing chat messages
5. Routing

## Html Pages:
home
login
user_registration_form
uber - This is the landing page html
map
chatbox
driver_signup
dashboard

## How to run the application
open a terminal and navigate to the project directory then
navigate to the web_flask directory and run "python3 -m user_registration_form"
-----------------------------------------------------------------------------------------------------

# Accessing the home page
open a browser and paste in the url "http://0.0.0.0:5001/" or "http://0.0.0.0:5001/home"
-----------------------------------------------------------------------------------------------------

# passenger sign up and driver sign up
You can sign up as a passenger or driver by using the individual sign up buttons for both driver or passener
-----------------------------------------------------------------------------------------------------
# Login In
Once you sign up as a passenger or driver. You can Log in and be redirected to the dashboard.
No need to login in again even after refreshing
-----------------------------------------------------------------------------------------------------
# Dashboard
On the dashboard you have option of 'logout', 'chat Now', 'go to Map', 'Book a ride' and 'get ride request'. 
Note:
1. Passengers can book a ride but can not receive ride requests. Hence no 'get ride request' option
2. Drivers can receive ride request but can not book a ride. Hence 'no book a ride' option
------------------------------------------------------------------------------------------------------
# Chatting
The 'chat Now' is available only after
1. As a Passenger you book a ride.
2. As a driver, you have gotten a ride request.
-----------------------------------------------------------------------------------------------------

# Ride Request
As a driver logged in. You must enable the 'get ride request' before a passenger books a ride or 
you would not get their ride request notification.
Note:
1. You can only receive ride requests from passengers when you enable/click the 'get ride request'  button at the dashboard
-----------------------------------------------------------------------------------------------------

# Book Ride
As a passenger logged in. Try to book a ride. You can click on the button multiple times, it toggles revealing the form for ride details and hiding it consequently.
-----------------------------------------------------------------------------------------------------

# Map
The 'Go to Map' button helps to plot the best route from user current position to selected destination after booking a ride. You can always selected a different starting point at the map interface or go back to dashboard 'Go to dashboard'
-----------------------------------------------------------------------------------------------------

# Algorithm
1. In case of enabling/clicking the get request for multiple drivers logged in. The application priorities distance/closeness to the passenger location and sends the ride request only to the nearest driver.
2. If a driver receives a ride request, the driver has the option of accepting or rejecting the ride. 
if the driver rejects the ride, the ride request is sent to next driver based on proximity.
-----------------------------------------------------------------------------------------------------

## Remember
1. You can un comment the navigator geolocation used within the script tag to optain accurate data as the one used are random variables to demonstrate the applications performance. Check the test.html file for the code to apply navigator geolocation.
2. During application testing, copy and paste the url "http://0.0.0.0:5001/" in different windows of the same or different browsers.
3. Have Fun

## more ......
## Thank You.
