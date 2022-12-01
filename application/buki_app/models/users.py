from buki_app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship
#from buki_app.models.chats import Chat


class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(100))
    displayname = db.Column(db.String(100))
    biotext = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    chats = relationship("Chat",primaryjoin="or_(User.id==Chat.user_a_id, User.id==Chat.user_b_id)",
                         order_by="desc(buki_app.models.chats.Chat.last_update)")

    def __init__(self,
                 username,
                 password,
                 displayname=None,
                 biotext=None,
                 profilepictureurl=None):
        self.username = username
        self.password = password
        self.biotext = biotext
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return '<Entry id:{} Username:{}'.format(self.id, self.username)

    

    def checkMessageIDMatch(self, id):
        cIDs = [c.id for c in self.chats]
        return id in cIDs
