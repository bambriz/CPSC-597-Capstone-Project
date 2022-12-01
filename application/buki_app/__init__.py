from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder="templates")
app.config.from_object('buki_app.config')
db = SQLAlchemy(app)
app.app_context().push()

from buki_app.views import views, chats

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from buki_app.models.users import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
	return User.query.get(int(user_id))

from buki_app.models.chats import Chat
from buki_app.models.users import User
from buki_app.models.messages import Message

with app.app_context():
    db.create_all()