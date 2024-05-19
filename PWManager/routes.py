from flask import jsonify, request, session, render_template, redirect, flash, url_for
from app import app, db
from models import User, Post
from password import verify_password_requirements, hash_pw, check_password

@app.route('/', methods=['GET', 'POST'])
def start_app():
    if not session.get('logged_in', False):
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

# Register a master user with a master password
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash("Passwords do not match", 'error')
            return redirect(url_for('register'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Username or Email already in use', 'error')
            return redirect(url_for('register'))
        
        verified, msg = verify_password_requirements(password1)
        if not verified:
            flash(msg)
            return redirect(url_for('register'))

        hashed_password = hash_pw(password1)
        new_user = User(username=username, email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful", 'message')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(str(e), 'error')
            return redirect(url_for('register'))
        
    return render_template('register.html')

# Login with either username or email
@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in', False):
        if request.method == 'POST':
            identifier = request.form['identifier']
            password = request.form['password']
            user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

            if user and check_password(password, user.password_hash):
                session['logged_in'] = True
                session['user_id'] = user.id
                return redirect('/dashboard')
            else:
                flash('Invalid Credentials', 'error')  # Adding an error message

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Handle user creation logic here
        pass
    return render_template('create_user.html')

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        # Handle user search logic here
        pass
    return render_template('search_user.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You have been logged out.', 'message')
    return redirect(url_for('login'))