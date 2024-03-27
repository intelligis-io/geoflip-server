from datetime import timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schemas import UserSchema, LoginSchema

UserBlueprint = Blueprint("Users", __name__, description="Operations on users")

@UserBlueprint.route("/register")
class UserRegister(MethodView):
    #apply the schema to the incoming data this ensures that we are getting the data from the user in the correct format
    @UserBlueprint.arguments(UserSchema, description="User data", example={"username":"test", "email":"test@user.com", "password":"test"})
    def post(self, user_data):
        if UserModel.query.filter_by(email=user_data["email"]).first():
            abort(400, message="email already exists.")
        if UserModel.query.filter_by(username=user_data["username"]).first():
            abort(400, message="username already exists.")
        
        user = UserModel(
            email=user_data["email"],
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="An error occurred while adding the user to the database.")

        return {"message":"User created."}, 201

@UserBlueprint.route("/user/<int:user_id>")
class User(MethodView):
    # ensures that we are returning the data in the correct format
    @UserBlueprint.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message="An error occurred while deleting the user.")

        return {"message":"User deleted."}, 200

@UserBlueprint.route("/users")
class UsersList(MethodView):
    # ensures that we are returning the data in the correct format
    @UserBlueprint.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

@UserBlueprint.route("/login")
class UserLogin(MethodView):
    @UserBlueprint.arguments(LoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(email=user_data["email"]).first()
        
        if not user or not pbkdf2_sha256.verify(user_data["password"], user.password):
            abort(401, message="Invalid credentials.")
        else:
            # create an access token for the user
            expires_in = timedelta(minutes=30)
            access_token = create_access_token(identity=user.user_id, expires_delta=expires_in)
            return {"access_token":access_token}, 200

@UserBlueprint.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"User logged out."}, 200