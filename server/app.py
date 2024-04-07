from flask import Flask, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session
from utils import encrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'TEST_KEY'
app.config["MONGO_URI"] = "mongodb://localhost:27017/passwordManagerDB"
mongo = PyMongo(app)
try:
    mongo.db.users.find_one()
    print("Connected to MongoDB.")
except:
    print("Fail to connect to DB")

@app.route('/')
def index():
    return "Welcome to the Security+ Password Manager"

# 配置OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='616979386644-q631gp05jl84popmo485hj8sul6pjuv0.apps.googleusercontent.com',
    client_secret='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',
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
    users = mongo.db.users
    # Get username, password and current url
    username = request.json['username']
    preferred_password = request.json['password']
    url = request.json['url']

    user = users.find_one({'username': username})
    if user:
        # Encrypt new string (website + password)
        encrypted_password = encrypt(preferred_password + url)
        # Save the encrypt password to DB
        users.update_one({'_id': user['_id']}, {'$push': {'websites': {'url': url, 'passwordHash': encrypted_password}}})
        return jsonify({"message": "Password encrypted and saved successfully"}), 200

    return jsonify({"message": "User not found"}), 404


@app.route('/get-password', methods=['POST'])
def get_password():
    username = request.json['username']
    preferred_password = request.json['password']
    url = request.json['url']

    user = mongo.db.users.find_one({'username': username})
    if user:
        encrypted_password = encrypt(preferred_password + url)
        for website in user.get('websites', []):
            if website['url'] == url and website['passwordHash'] == encrypted_password:
                return jsonify({"encryptedPassword": encrypted_password}), 200
        return jsonify({"message": "No matching encrypted password found"}), 404
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
