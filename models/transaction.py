from db import db
from datetime import datetime

class TransactionModel(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    description = db.Column(db.String(255))

    usages = db.relationship('UsageModel', backref='transaction', lazy='dynamic')

    