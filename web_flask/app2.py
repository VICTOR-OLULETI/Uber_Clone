from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index2.html')

@socketio.on('connect')
def on_connect():
    print('User connected')

@socketio.on('join')
def on_join(data):
    room = 'driver'
    join_room(room)
    print('User joined room: driver')

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    print(f'User left room: {room}')

@socketio.on('passenger_request')
def handle_passenger_request(userType):
    emit('driver_request', broadcast=True)
                                 
    print(f'Passenger joined room: driver')

@socketio.on('driver_response')
def handle_driver_response(data):
    #room = data['room']
    print(f'which room is this: passenger or driver') #just checking progress here
    emit('passenger_response', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
