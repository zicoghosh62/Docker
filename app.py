from flask import Flask, request, render_template, redirect, session
from pymongo import MongoClient
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

# MongoDB configuration
mongo_uri = os.getenv('MONGO_URI', 'mongodb://root:example@mongo:27017/userdata')
client = MongoClient(mongo_uri)
db = client.get_database("userdata")
users_collection = db.get_collection("users")

@app.route('/')
def index():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if the email is already registered
        if users_collection.find_one({'email': email}):
            return render_template('register.html', error='Email already registered.')

        # Hash the password and save the user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        users_collection.insert_one({
            'name': name,
            'email': email,
            'password': hashed_password
        })
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({'email': email})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['email'] = user['email']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid email or password.')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = users_collection.find_one({'email': session['email']})
        return render_template('dashboard.html', user=user)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

