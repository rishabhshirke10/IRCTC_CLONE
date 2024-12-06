from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from flask_mysql_connector import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = "your_secret_key_987"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key_876"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Rishabh@10"
app.config["MYSQL_DATABASE"] = "railway_system"

jwt = JWTManager(app)
mysql = MySQL(app)

# ----------------------------
# Routes for HTML Templates
# ----------------------------


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/trains", methods=["GET"])
def trains_page():
    if "source" in request.args and "destination" in request.args:
        # This handles the GET /trains for checking train availability
        source = request.args.get("source")
        destination = request.args.get("destination")
        cursor = mysql.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM trains WHERE source = %s AND destination = %s",
            (source, destination),
        )
        trains = cursor.fetchall()
        return jsonify(trains), 200
    return render_template("check_trains.html")  # Renders the form for user input


@app.route("/add_train", methods=["GET"])
def add_train_page():
    return render_template("add_train.html")


@app.route("/book", methods=["GET"])
def book_page():
    return render_template("book.html")


@app.route("/bookings", methods=["GET"])
def bookings_page():
    return render_template("bookings.html")


# ----------------------------
# API Endpoints
# ----------------------------


# Register User
@app.route("/register", methods=["POST"])
def register():
    # Handle both JSON and form-encoded data
    if request.content_type == "application/json":
        data = request.json
    else:
        data = request.form

    # Validate required fields
    if not all(key in data for key in ("username", "password", "role")):
        return jsonify({"error": "Missing required fields"}), 400

    username = data["username"]
    password = generate_password_hash(data["password"])
    role = data["role"]

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, password, role),
    )
    conn.commit()
    return jsonify({"message": "User registered successfully"}), 201


# Login User
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and check_password_hash(user["password"], password):
        access_token = create_access_token(
            identity={"id": user["id"], "role": user["role"]}
        )
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


# Add Train (Admin Only)
@app.route("/trains", methods=["POST"])
@jwt_required()
def add_train():
    claims = get_jwt_identity()
    role = claims.get("role")
    if role != "admin":
        return jsonify({"message": "Admins only!"}), 403

    data = request.json
    name = data["name"]
    source = data["source"]
    destination = data["destination"]
    total_seats = data["total_seats"]

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trains (name, source, destination, total_seats, available_seats) VALUES (%s, %s, %s, %s, %s)",
        (name, source, destination, total_seats, total_seats),
    )
    conn.commit()
    return jsonify({"message": "Train added successfully"}), 201


# Book Seat
@app.route("/book", methods=["POST"])
@jwt_required()
def book_seat():
    user = get_jwt_identity()
    data = request.json
    train_id = data["train_id"]

    conn = mysql.connection
    cursor = conn.cursor(dictionary=True)

    # Check seat availability
    cursor.execute("SELECT * FROM trains WHERE id = %s", (train_id,))
    train = cursor.fetchone()

    if not train or train["available_seats"] <= 0:
        return jsonify({"message": "No seats available"}), 400

    # Update seat availability and create booking
    cursor.execute(
        "UPDATE trains SET available_seats = available_seats - 1 WHERE id = %s",
        (train_id,),
    )
    cursor.execute(
        "INSERT INTO bookings (user_id, train_id, seat_number) VALUES (%s, %s, %s)",
        (user["id"], train_id, train["total_seats"] - train["available_seats"] + 1),
    )
    conn.commit()
    return jsonify({"message": "Seat booked successfully"}), 201


# Get Booking Details
@app.route("/bookings", methods=["POST"])
@jwt_required()
def get_bookings():
    user = get_jwt_identity()
    user_id = user["id"]

    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookings WHERE user_id = %s", (user_id,))
    bookings = cursor.fetchall()
    return jsonify(bookings), 200


@app.route("/", methods=["GET"])
def home_page():
    return render_template("home.html")


# ----------------------------
# Main Application
# ----------------------------


if __name__ == "__main__":
    app.run(debug=True)
