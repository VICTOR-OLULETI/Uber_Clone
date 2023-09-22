from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure secret key

# Database setup
# Database setup for mysql even though it wasn't used
DATABASE = {
    "user": "username",
    "password": "your password",
    "host": "localhost",
    "database": "Uber"
}

def get_db():
    db = mysql.connector.connect(**DATABASE)
    return db

# API endpoint to receive and store passenger and ride details
@app.route('/book_ride', methods=['GET', 'POST'])
def book_ride():
    if request.method == "POST":
        #passenger_name = data.get('passenger_name')
        selected_ride = request.form['selected_ride']
        selected_destination =request.form['selected_destination']
        estimated_fare = request.form['estimated_fare']

        # Store the data in the database
        try:
            db = get_db()
            cur = db.cursor()
            cur.execute("INSERT INTO bookings (selected_ride, selected_destination, estimated_fare) VALUES (%s, %s, %s)",
                        (selected_ride, selected_destination, estimated_fare))
            db.commit()
            #cur.close()
            return redirect(url_for("book_ride"))
        except mysql.connector.IntegrityError:
            flash("Not registered", "error")
    return (render_template('passenger_home_screen.html'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
