from flask import Flask
from dotenv import load_dotenv 

def create_app():
    app = Flask(__name__)
    load_dotenv()

    @app.get("/")
    def get_hello():
        return {"hello": "world"}, 200

    return app