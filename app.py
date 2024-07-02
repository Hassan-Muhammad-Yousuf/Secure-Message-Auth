from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Mock user data (for demonstration purposes)
users = {
    'john': {
        'username': 'john',
        'password_hash': generate_password_hash('password123')
    },
    'jane': {
        'username': 'jane',
        'password_hash': generate_password_hash('pass123')
    }
}

# Function to generate JWT token
def generate_jwt(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)  # Token expires in 30 days
    }
    jwt_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return jwt_token

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    username = auth.get('username', None)
    password = auth.get('password', None)

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    if username in users and check_password_hash(users[username]['password_hash'], password):
        jwt_token = generate_jwt(username)
        return jsonify({'token': jwt_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


if __name__ == '__main__':
    app.run(debug=True)
