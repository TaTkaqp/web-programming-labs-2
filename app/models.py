from datetime import datetime
from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)

    # Устанавливаем связи с сообщениями
    messages_sent = db.relationship('Message', backref='sender', lazy=True, foreign_keys='Message.sender_id', cascade="all, delete-orphan")
    messages_received = db.relationship('Message', backref='receiver', lazy=True, foreign_keys='Message.receiver_id', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}>'

    def is_admin(self):
        return self.role == 'admin'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
