from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import LoginManager,login_user, logout_user, login_required, current_user
from db import *
from user import * 
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
app.secret_key = 'secret key'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    message = ''
    if request.method == 'POST':
        username = request.form.get("username")
        print(f'username is {username}')
        password_input = request.form.get("password")
        user = get_user(username)
        print(f'User info is {user}')

        if user and user.check_password(password_input):
            login_user(user)
            
            return redirect(url_for('home'))
        else:
            message = 'Failed to login!'

    return render_template('login.html', message=message)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    message = ''
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            user = save_user(username, email, password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = "User already exists!"    
    return render_template('signup.html', message=message)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chatbox.html', username=username, room=room)
    else:
        return redirect(url_for('home'))

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has send message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined th room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit("join_room_announcement", data, room=data['room'])

@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data["username"], data['room']))
    leave_room(data['room'])
    socketio.emit("leave_room_announcement", data, room=data['room'])

@login_manager.user_loader
def load_user(username):
    return get_user(username)

if __name__ == "__main__":
    socketio.run(app, debug=True)