from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources import SuperUser, UserSignUp, UserSignIn, Tweet
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # to tell sqlalchemy to connect to sqlite data.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # If True, sqlalchemy will track the modifications so it will took some resources
app.config["JWT_SECRET_KEY"] = "super-secret"
api = Api(app)

JWT = JWTManager(app)

@app.before_first_request # this decorator will run the method before first request
def create_tables(): # this method will create tables base on column in models package
    db.create_all()

api.add_resource(UserSignUp, "/signup")
api.add_resource(UserSignIn, "/signin")
api.add_resource(SuperUser, "/users")
api.add_resource(Tweet, "/tweet")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)