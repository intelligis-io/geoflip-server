from db import db

class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)

    tokens = db.relationship('TokenModel', backref='user', lazy='dynamic')
    transactions = db.relationship('TransactionModel', backref='user', lazy='dynamic')