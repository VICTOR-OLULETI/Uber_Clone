from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATABASE = {
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "host": "localhost",
    "database": "your_database_name"
}

def get_db():
    db = mysql.connector.connect(**DATABASE)
    return db

@app.route("/driver_signup", methods=["POST"])
def driver_signup():
    data = request.json

    fullname = data.get('fullname')
    email = data.get('email')
    vehicle = data.get('vehicle')

    if not fullname or not email or not vehicle:
        flash("All fields are required", "error")
        return redirect(url_for("driver_signup"))

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO drivers (fullname, email, vehicle) VALUES (%s, %s, %s)",
                        (fullname, email, vehicle))
        db.commit()
        flash("Driver signup successful", "success")
        return redirect(url_for("driver_signup"))
    except mysql.connector.IntegrityError:
        flash("Email already registered", "error")

    return render_template("driver_signup.html")

if __name__ == "__main__":
    app.run(debug=True)




