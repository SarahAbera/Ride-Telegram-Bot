import pymysql

# Establish a connection to the MySQL database
db_connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="MyNewPass",
    database="tg_bot"
)

# Create a cursor object
db_cursor = db_connection.cursor()

def get_all_ride_requests():
    db_cursor.execute("select * from ride_request")
    ride_requests = db_cursor.fetchall()
    return ride_requests

def get_user(userId):
    db_cursor.execute("SELECT * FROM Ride_bot_user_info WHERE user_id = %s", (userId,))
    user = db_cursor.fetchone()
    return user

def check_user_exists(userId):
    db_cursor.execute("SELECT COUNT(*) FROM Ride_bot_user_info WHERE user_id = %s", (userId,))
    result = db_cursor.fetchone()
    return result

def update_user_profile(id, name, phoneNo, role):
    query = "UPDATE Ride_bot_user_info SET full_name = %s, phone = %s, role = %s WHERE user_id = %s"
    db_cursor.execute(query, (name, phoneNo, role, id))
    db_connection.commit()

def get_drivers():
    db_cursor.execute("SELECT * FROM Ride_bot_user_info WHERE role = 'driver'")
    drivers = db_cursor.fetchall()
    return drivers

def delete_user(user_id):
    query = "DELETE FROM Ride_bot_user_info WHERE user_id = %s"
    db_cursor.execute(query=query, args=(user_id,))
    db_connection.commit()

def get_history(user_id):
    db_cursor.execute("SELECT * FROM history WHERE id = %s", (user_id,))
    result = db_cursor.fetchall()
    return result

def remove_ride_request(id):
    query = "DELETE FROM ride_request WHERE user_id = %s"
    db_cursor.execute(query=query, args=(id,))
    db_connection.commit()

def insert_into_ride_bot_table(userId,full_name,phone,role):
    db_cursor.execute("""
        INSERT INTO Ride_bot_user_info (user_id, full_name, phone, role)
        VALUES (%s, %s, %s, %s)
    """, (userId, full_name, phone, role))
    db_connection.commit()

def insert_into_history_table(id, start, destination, price, date):
    query = "INSERT INTO history (id, start, destination, price, date) VALUES(%s, %s, %s, %s, %s)"
    db_cursor.execute(query, (id, start, destination, price, date))
    db_connection.commit()

def insert_into_ride_request(passenger_id,start,destination,price):
    db_cursor.execute("""
        INSERT INTO ride_request (id, starting_location, destination, price)
        VALUES (%s, %s, %s, %s)
    """, (passenger_id, start, destination, price))
    db_connection.commit()
