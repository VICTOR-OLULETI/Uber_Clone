from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'your_database_host'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/send_location', methods=['POST'])
def send_location():
    # Extract data from the request
    data = request.json
    driver_id = data.get('driver_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Store the location in the database
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO locations (driver_id, latitude, longitude) VALUES (%s, %s, %s)",
                (driver_id, latitude, longitude))
    mysql.connection.commit()
    cur.close()

    # Broadcast the update to connected clients
    socketio.emit('location_update', data, broadcast=True)

    return jsonify({"message": "Location sent successfully"})

@app.route('/get_location/<driver_id>', methods=['GET'])
def get_location(driver_id):
    # Retrieve the latest location from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT latitude, longitude FROM locations WHERE driver_id = %s ORDER BY id DESC LIMIT 1", (driver_id,))
    location = cur.fetchone()
    cur.close()
    return jsonify(location)
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
