import os
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurations for MySQL database connection
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')

mysql = MySQL(app)

# Route for checking if the server is running
@app.route('/')
def home():
    return "Server is running!"

# Route for retrieving data from the database
@app.route('/users', methods=['GET'])
def fetch_users():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)

# Route for adding data to the database
@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Users (Fname, Age) VALUES (%s, %s)", 
                   (user_data['name'], user_data['age']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User added successfully'})

# Route for updating user data in the database
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Users SET Fname = %s, Age = %s WHERE Uid = %s", 
                   (user_data['name'], user_data['age'], user_id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User updated successfully'})

# Route for deleting user data from the database
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Users WHERE Uid = %s", (user_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User deleted successfully'})

# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT'), debug=True)
