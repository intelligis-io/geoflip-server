from db import db

class TokenModel(db.Model):
    __tablename__ = "tokens"

    token_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(256), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    usages = db.relationship('UsageModel', backref='token', lazy='dynamic')

    