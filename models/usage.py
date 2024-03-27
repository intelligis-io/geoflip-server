from db import db
from datetime import datetime

class UsageModel(db.Model):
    __tablename__ = "usage"

    usage_id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('tokens.token_id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    endpoint = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    request_size = db.Column(db.Integer, nullable=False)
    response_size = db.Column(db.Integer, nullable=False)