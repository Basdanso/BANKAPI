from flask import Flask, request, jsonify, json
from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Controller.account_dao_Postgres import AccountDaoPostgres
from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Controller.user_dao_postgres import UserDaoPostgres
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Exceptions.value_type_error import ValueTypeError
from Python_Bank_Api.Models import users
from Python_Bank_Api.Models.users import User, user
from Python_Bank_Api.Services.account_service import AccountServices
from Python_Bank_Api.Services.account_service_impl import AccountServiceImpl
from Python_Bank_Api.Services.user_service import UserServices
from Python_Bank_Api.Services.user_service_impl import UserServiceImpl

user_dao: UserDAO = UserDaoPostgres()
user_service: UserServices = UserServiceImpl(user_dao)

account_dao: AccountDAO = AccountDaoPostgres()
account_service: AccountServices = AccountServiceImpl(account_dao, user_dao)


def create_user_route(app: Flask):
    @app.route('/users', methods=['POST'])
    def post_user():
        user = User.as_json_dict(request.json)
        user_service.create_user(user)
        app.logger.info(f'Created new user with ID: {user.uid}')
        return jsonify(user.as_json_dict()), 201

    @app.route('/user', methods=['GET'])
    def get_all_users():
        try:
            customers = user_service.get_all_users()
            app.logger.info(f' Get all users ')
            return jsonify([user.as_json_dict() for user in users]), 200
        except ResourceNotFoundError as e:
            return str(e)

    @app.route("/user/<uid>", methods=["GET"])
    def get_user_by_id(uid: str):

        try:
            if not uid.isnumeric():
                raise ValueTypeError
            customer = user_service.get_user_by_id(int(uid))
            app.logger.info(f'get user by with Id: {user.uid}')
            return jsonify(User.as_json_dict())
        except ValueTypeError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/user/<uid>", methods=["PUT"])
    def update_user_by_id(uid):

        try:
            if not uid.isnumeric():
                raise ValueTypeError
            user_service.get_user_by_id(int(uid))
            user = User.as_json_dict(request.json)
            user.uid = int(uid)
            user = user_service.update_user(user)
            app.logger.info(f'User with Id:{user.uid} updated successfully')
            return jsonify(user.as_json_dict())
        except ValueTypeError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.route("/user/uid/<uid>", methods=["DELETE"])
    def delete_user_by_id(uid: str):
        try:
            if not uid.isnumeric():
                raise ValueTypeError
            account_service.delete_account_by_user_id(int(uid))
            if not uid.isnumeric():
                raise ValueTypeError
            user_service.delete_user_by_id(int(uid))
            app.logger.info(f'deleted user with Id: {int(uid)}')
            return f"User with Id: {int(uid)}  Deleted successfully", 205
        except ValueTypeError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404