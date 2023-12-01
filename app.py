from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection parameters
db_config = {
    'host': 'testdatabase.cnucxjl9epx6.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'bitcot2023',
    'database': 'bitcot'
}

@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.json.get('id')
    username = request.json.get('username')
    age = request.json.get('age')

    if not (user_id and username and age):
        return jsonify({'error': 'Missing data'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            query = "INSERT INTO users (id, username, age) VALUES (%s, %s, %s)"
            values = (user_id, username, age)

            cursor.execute(query, values)
            conn.commit()

            return jsonify({'message': 'User added successfully'}), 200
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
