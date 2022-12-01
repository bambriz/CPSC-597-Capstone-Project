#buki_app/views.py
from flask import request, redirect, url_for, render_template, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from buki_app import app
from buki_app import db
from buki_app.models.users import User
from flask_login import login_user, login_required, current_user, logout_user
import datetime
from buki_app.models.chats import Chat
from buki_app.models.messages import Message
from sqlalchemy import or_


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userName = request.form.get('username')
        password = request.form.get('password')
        # passwordConfirm = request.form.get('passwordconfirm')

        user = User.query.filter_by(username=userName).first()
        if user:
            flash('Username is already taken')
            return redirect(url_for('signup'))
        if len(password) < 8:
            flash('Password must be at least 8 characters long')
            return redirect(url_for('signup'))
        new_user = User(username=userName,
                        password=generate_password_hash(password,
                                                        method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        flash('Account Creation Successful')
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = user = User.query.filter_by(username=username).first()

        if not user:
            flash('User name is different')
        elif not check_password_hash(user.password, password):
            flash('Password is different')
        else:
            login_user(user, remember=remember)
            session['logged_in'] = True
            flash('Login successful')
            return redirect(url_for('profile'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Logged Out')
    return redirect(url_for('welcome'))


@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('welcome'))
    chats = Chat.query.filter_by(user_a_id=current_user.id).all()
    chatsTwo = Chat.query.filter_by(user_b_id=current_user.id).all()
    print(chats)
    chats= chats+chatsTwo
    
    return render_template('profile.html',
                           name=current_user.username,
                           chats=chats)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
