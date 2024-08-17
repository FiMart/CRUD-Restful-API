from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'user': 'root',
    'password': 'passwd', # password in mysql connection
    'host': '127.0.0.1',
    'database': 'userdb'
}

# Helper function to connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/user/', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

@app.route('/user/<int:uid>', methods=['GET'])
def get_user(uid):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE uid = %s", (uid,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user/new', methods=['POST'])
def create_user():
    new_user = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (uid, name, age) VALUES (%s, %s, %s)",
                   (new_user['uid'], new_user['name'], new_user['age']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User created', 'uid': new_user['uid']}), 201

@app.route('/user/<int:uid>', methods=['PUT'])
def update_user(uid):
    update_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s, age = %s WHERE uid = %s",
                   (update_data['name'], update_data['age'], uid))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User updated'})

@app.route('/user/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE uid = %s", (uid,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'User deleted'})

if __name__ == '__main__':
    app.run(debug=True)
