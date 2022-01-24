from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime

from models import UserModel

class UserSignUp(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type = str,
        required = True,
        help = "This is a mandatory key"
    )
    parser.add_argument(
        "password",
        type = str,
        required = True,
        help = "This is a mandatory key"
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "{} already exists".format(data["username"])}, 400 # Bad Request
        
        user = UserModel(**data)
        try:
            user.save_to_db()
        except:
            return {"message": "An error occured"}, 500 # Internal Server Error
        return user.json(), 201 # Created


class UserSignIn(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type = str,
        required = True,
        help = "This is a mandatory key"
    )
    parser.add_argument(
        "password",
        type = str,
        required = True,
        help = "This is a mandatory key"
    )

    @classmethod
    def get(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username_pass(**data)
        if user is None:
            return {"message": "Wrong username or password"}, 400 # Bad Request

        access_token = create_access_token(identity={"username": data["username"]})
        return {"access_token": access_token}, 200


class Tweet(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "tweet",
        type = str,
        required = True,
        help = "This is a mandatory key"
    )

    @classmethod
    @jwt_required() # this func below required a token
    def get(cls):
        data = cls.parser.parse_args()
        current_user = get_jwt_identity()
        return {
            "username": current_user["username"], 
            "tweet": data["tweet"],
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }, 200
        

class SuperUser(Resource):
    @jwt_required() # this func below required a token
    def get(self):
        current_user = get_jwt_identity()
        if current_user["username"] == "admin":
            return {'users': [user.json() for user in UserModel.query.all()]}, 200
        return {"message": "Admin required"}, 400 # Bad Request