from flask import jsonify, request, session, render_template, redirect, flash
from run import app, db
from models import User, Post
from password import verify_password_requirements, hash_pw, check_password

@app.route('/users')
def list_users():
    users = User.query.all()
    return jsonify([{'username': user.username, 'email': user.email} for user in users])

@app.route('/posts')
def list_posts():
    posts = Post.query.all()
    return jsonify([{
        'title': post.title,
        'body': post.body,
        'author': post.author.username,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for post in posts])

# Register a master user with a master password
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 == password2:
            verified, msg = verify_password_requirements(password1)
            if not verified:
                flash(msg, 'error')
            else:
                hashed_password = hash_pw(password1)
                new_user = User(username=username, email=email, password=hashed_password)

                try:
                    db.session.add(new_user)
                    db.session.commit()

                    flash("Registeration Successful", 'message')
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'error' : str(e)}), 500
        else:
            flash("Passwords do not match", 'error')

# Login with either username or email
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

        if user and check_password(password, user.password_hash):
            session['user_id'] = user.id
            return redirect('templates/dashboard.html')  # Assuming there is a dashboard endpoint
        else:
            flash('Invalid Credentials', 'error')  # Adding an error message

    return render_template('login.html')
