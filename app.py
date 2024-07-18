from flask import Flask, request, render_template, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, email, password, username):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    message = session.pop('message', None)  # Get and remove the message from session
    return render_template('index.html', username=session.get('username'), message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        new_user = User(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['email'] = user.email
            return redirect(url_for('index'))
        else:
            return "Invalid email or password!"
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))

# Components of pages

@app.route('/home')
def home():
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('About us.html')

@app.route('/skill')
def skill():
    return render_template('skill.html')

if __name__ == '__main__':
    app.run(debug=True)
