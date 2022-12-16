from buki_app import db
from datetime import datetime
from sqlalchemy.orm import relationship


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    author = db.Column(db.String(32))
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chats.id'))

    def __init__(self, text, author,chat_id):
        self.text = text
        self.chat_id = chat_id
        self.author = author
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
       return '<Msg id:{} Text:{} Author:{}'.format(self.id, self.text, self.author)

    def getPassedTimeStamp(self):
        current = datetime.utcnow() - self.timestamp
        minutes = divmod(current.total_seconds(), 60)
        return f'{int(minutes[0])} minutes and {int(minutes[1])} seconds'
