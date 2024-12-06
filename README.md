# IRCTC_CLONE
Railway Management System API (IRCTC Clone)
Here's a sample `README.md` file for your railway management system project:

---

# Railway Management System API (IRCTC Clone)

A web-based API that simulates a railway management system, allowing users to check train availability, book seats, and admins to manage train data.

---

## **Features**
- **User Features**:
  - Register and login.
  - Check seat availability between two stations.
  - Book a seat on available trains.
  - Fetch booking details.
  
- **Admin Features**:
  - Add trains with details like source, destination, and seat capacity.

- **Concurrency Handling**:
  - Prevent race conditions during simultaneous seat bookings.

---

## **Tech Stack**
- **Backend**: Python (Flask)
- **Database**: MySQL

---

## **Setup Instructions**

### Prerequisites
1. Python 3.8+
2. MySQL Server
3. Package Manager: `pip`

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository_link>
   cd <repository_directory>
   ```

2. Install dependencies:
   ```bash
   pip install flask flask-jwt-extended flask-mysql-connector werkzeug
   ```

3. Create the database:
   - Open MySQL shell and execute the commands in the [database setup](#database-setup) section.

4. Configure the MySQL connection in `app.py`:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'your_mysql_user'
   app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
   app.config['MYSQL_DATABASE'] = 'railway_system'
   ```

5. Start the server:
   ```bash
   python app.py
   ```
   The server will run on `http://127.0.0.1:5000`.

---

## **API Endpoints**

### **User Endpoints**
1. **Register**  
   **POST** `/register`  
   - **Request Body**:
     ```json
     {
       "username": "user123",
       "password": "password123",
       "role": "user"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "User registered successfully"
     }
     ```

2. **Login**  
   **POST** `/login`  
   - **Request Body**:
     ```json
     {
       "username": "user123",
       "password": "password123"
     }
     ```
   - **Response**:
     ```json
     {
       "access_token": "your_jwt_token"
     }
     ```

3. **Check Train Availability**  
   **GET** `/trains?source=<source>&destination=<destination>`  
   - **Response**:
     ```json
     [
       {
         "id": 1,
         "name": "Express Train",
         "source": "City A",
         "destination": "City B",
         "total_seats": 100,
         "available_seats": 50
       }
     ]
     ```

4. **Book a Seat**  
   **POST** `/book`  
   - **Request Headers**:
     ```
     Authorization: Bearer <access_token>
     ```
   - **Request Body**:
     ```json
     {
       "train_id": 1
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Seat booked successfully"
     }
     ```

5. **Get Booking Details**  
   **GET** `/bookings`  
   - **Request Headers**:
     ```
     Authorization: Bearer <access_token>
     ```
   - **Response**:
     ```json
     [
       {
         "id": 1,
         "train_id": 1,
         "seat_number": 5
       }
     ]
     ```

---

### **Admin Endpoints**
1. **Add Train**  
   **POST** `/trains`  
   - **Request Headers**:
     ```
     Authorization: Bearer <admin_token>
     ```
   - **Request Body**:
     ```json
     {
       "name": "Express Train",
       "source": "City A",
       "destination": "City B",
       "total_seats": 100
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Train added successfully"
     }
     ```

---

## **Database Setup**
```sql
CREATE DATABASE railway_system;

USE railway_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('user', 'admin') NOT NULL
);

CREATE TABLE trains (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    total_seats INT NOT NULL,
    available_seats INT NOT NULL
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    train_id INT NOT NULL,
    seat_number INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (train_id) REFERENCES trains(id)
);
```

---

## **Testing**
- Use **Postman** or **curl** to test the endpoints.
- Example Postman collection:
  - Register a user
  - Login to get a token
  - Check trains between two stations
  - Book a seat and fetch booking details


