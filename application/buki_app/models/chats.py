from buki_app import db
from datetime import datetime
#from buki_app.models.users import User
from buki_app.models.messages import Message
from sqlalchemy.orm import relationship


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.String(32))
    created_at = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    user_a_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_b_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    messages = relationship("Message",
                            order_by=Message.timestamp)

    def __init__(self, created_by=None, user_a_id=None, user_b_id=None):
        self.created_by = created_by
        self.created_at = datetime.utcnow()
        self.last_update = self.created_at
        self.user_a_id = user_a_id
        self.user_b_id = user_b_id

    def __repr__(self):
       return '<Chat id:{} User A:{} User B:{}'.format(self.id, self.user_a_id, self.user_b_id)
