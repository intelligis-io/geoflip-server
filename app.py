import os
from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv 

from db import db
import models

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # construct database url
    db_user = os.getenv('DB_USERNAME')
    db_pass = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_ssl_mode = os.getenv("DB_SSL")
    db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?sslmode={db_ssl_mode}"

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "GeoFlip REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.1.0"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    # creates all the tables before the first request
    with app.app_context():
        db.create_all()

    @app.get("/")
    def get_hello():
        return {"hello": "world"}, 200

    return app