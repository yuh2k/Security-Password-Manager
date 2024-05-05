from flask import Flask, request, jsonify, redirect, url_for
from flask import render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session
from utils.encrypt import encrypt_password
from flask_cors import CORS
import os
from dotenv import load_dotenv
import hashlib
import requests

app = Flask(__name__)
CORS(app)
load_dotenv()
app.secret_key = os.environ.get('FLASK_APP_SECRET_KEY')
app.config["MONGO_URI"] = "mongodb://localhost:27017/passwordManagerDB"
mongo = PyMongo(app)
try:
    mongo.db.users.find_one()
    print("Connected to MongoDB.")
except:
    print("Fail to connect to DB")

@app.route('/')
def index():
    return render_template('index.html')

# OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth/callback')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    email = user_info.get('email')
    if email:
        session['user_email'] = email 
        user = mongo.db.users.find_one({'email': email})
        if user:
            print('Existing user:', email)
        else:
            mongo.db.users.insert_one({
                'email': email,
                'websites': []
            })
            print('New user created:', email)
    else:
        return jsonify({"message": "Failed to get user email from Google"}), 400
    return redirect(url_for('index'))

@app.route('/encrypt-and-save', methods=['POST'])
def encrypt_and_save():
    if 'user_email' not in session:
        return jsonify({"message": "User is not logged in"}), 401
    email = session['user_email']
    preferred_password = request.json['password']
    url = request.json['url']

    users = mongo.db.users
    user = users.find_one({'email': email})  
    if user:
        encrypted_password = encrypt_password(url + preferred_password)
        users.update_one({'_id': user['_id']}, {'$push': {'websites': {'url': url, 'passwordHash': encrypted_password}}})
        return jsonify({"message": "Password encrypted and saved successfully"}), 200

    return jsonify({"message": "User not found"}), 404

@app.route('/get-password', methods=['GET'])
def get_password():
    if 'user_email' not in session:
        return jsonify({"message": "User is not logged in"}), 401
    email = session['user_email']
    preferred_password = request.json['password']
    url = request.json['url']

    user = mongo.db.users.find_one({'email': email})
    if user:
        encrypted_password = encrypt_password(url + preferred_password)
        for website in user.get('websites', []):
            if website['url'] == url and website['passwordHash'] == encrypted_password:
                return jsonify({"encryptedPassword": encrypted_password}), 200
        return jsonify({"message": "No matching encrypted password found"}), 404
    else:
        return jsonify({"message": "User not found"}), 404


def get_password_sha1_hash(password):
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    return sha1.hexdigest().upper()

@app.route('/check-password-leak', methods=['POST'])
def check_password_leak():
    """ Check password"""
    password = request.json.get('password')
    if not password:
        return jsonify({"message": "Password is required"}), 400

    sha1_hash = get_password_sha1_hash(password)
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    
    response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
    if response.status_code == 200:
        hashes = (line.split(':') for line in response.text.splitlines())
        for hash_suffix, count in hashes:
            if hash_suffix == suffix:
                return jsonify({"message": "Password has been leaked", "leak_count": count}), 200
        return jsonify({"message": "Password has not been leaked"}), 200
    else:
        return jsonify({"message": "Error fetching data from pwnedpasswords.com"}), 500

@app.route('/check-login', methods=['GET'])
def check_login():
    if 'user_email' in session:
        return jsonify(loggedIn=True, email=session['user_email'])
    else:
        return jsonify(loggedIn=False)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_email', None)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)


