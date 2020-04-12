import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="This field cannot be left blank!")
        parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")

        def post(self):
            data = UserRegister.parser.parse_args()

            # Check that there are no repeating users:
            if UserModel.find_by_username(data['username']): #is not None
                return {"message": "User already exists"}, 400

            # data['username'], data['password'] = **data
            user = UserModel(**data)
            user.save_to_db()

            return {"message": "User created successfully."}, 201
