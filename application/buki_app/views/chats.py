from flask import request, redirect, url_for, render_template, flash, session
from buki_app import app
from buki_app import db
from buki_app.models.chats import Chat
from buki_app.models.messages import Message
from buki_app.models.users import User
from flask_login import current_user
from sqlalchemy import or_
from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length

@app.route('/')
def show_chats():
    if not current_user.is_authenticated:
        return redirect(url_for('welcome'))
    # if current_user.username != username:
    #     return redirect(url_for('welcome'))
    if not session.get('logged_in'):
        return redirect(url_for('welcome'))
    
    chats = Chat.query.filter_by(user_a_id=current_user.id).all()
    chatsTwo = Chat.query.filter_by(user_b_id=current_user.id).all()
    print(chats)
    chats= chats+chatsTwo
    
    return render_template('profile.html',name=current_user.username,chats = chats)

@app.route('/<username>/chats/<int:id>')
def show_chat(username,id):
    if not current_user.is_authenticated:
        return redirect(url_for('welcome'))
    if current_user.checkMessageIDMatch(id):
        chat = Chat.query.get(id)
    else:
        return redirect(url_for('welcome'))
    user_a_name = User.query.get(chat.user_a_id).username
    user_b_name = User.query.get(chat.user_b_id).username
    messages = Message.query.filter_by(chat_id=chat.id).order_by(Message.timestamp).all()
    return render_template('chats/show.html',chat=chat,messages=messages,user_a_name=user_a_name,user_b_name=user_b_name,username=username)

@app.route('/<username>/chats/new', methods=['GET'])
def new_chat(username):
    if not current_user.is_authenticated:
        return redirect(url_for('welcome'))
    return render_template('chats/new.html', name=username)

@app.route('/<username>/chats', methods=['POST'])
def add_chat(username):
    if not current_user.is_authenticated:
        return redirect(url_for('welcome'))
    user_b = User.query.filter_by(username = request.form['Recipient']).first()
    if not user_b:
        flash('Invalid Recipient, Try Again.')
        return redirect(url_for('new_chat'))
    #first check if a chat between users already exists
    #Current user will either be user A or User B
    #if current chat exists redirect to new chat
    chat = Chat.query.filter_by(user_a_id = current_user.id, user_b_id = user_b.id)
    #if this returns something try one more time
    if chat:
        chat = Chat.query.filter_by(user_a_id = user_b.id, user_b_id = current_user.id).first()
    #seems redundant to check again but it's important
    if chat:
        flash('A chat with {} already exists.'.format(user_b.username))
        return render_template('chats/new.html', name=username)
    chat = Chat(created_by=current_user.username, user_a_id = current_user.id, user_b_id = user_b.id)
    msg = Message(text=request.form['text'], author=current_user.username, chat_id=chat.id)
    db.session.add(chat)
    db.session.commit()
    db.session.add(msg)
    db.session.commit()
    flash("Chat Created")
    return redirect(url_for('show_chat',id=chat.id, username=current_user.username))
    #Add encrption to ass first message of chat

@app.route('/<username>/chats/<int:id>', methods=['POST'])
def new_reply(id,username):
	if "messagetext" in request.form:
			text = request.form['messagetext']
            
			author = current_user.username
			chat_id = id
			new_message = Message(text=text,author=author,chat_id=chat_id)
			new_message.save()
	return redirect(url_for('show_chat',username=current_user.username,id=id))



    


