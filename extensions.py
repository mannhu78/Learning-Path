from pymongo import MongoClient
from flask_login import LoginManager

client = MongoClient("mongodb://localhost:27017/")
db = client.learning_path

login_manager = LoginManager()
