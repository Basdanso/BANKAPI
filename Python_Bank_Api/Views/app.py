import body as body
import flask
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from Python_Bank_Api.Controller.account_dao_Postgres import AccountDaoPostgres
from Python_Bank_Api.Controller.account_dao_local import AccountDaoLocal
from Python_Bank_Api.Exceptions.Insufficient_fund import InsufficientFund
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Exceptions.value_type_error import ValueTypeError
from Python_Bank_Api.Models import users
from Python_Bank_Api.Models.accounts import Account
from Python_Bank_Api.Models.users import User, user
from Python_Bank_Api.Services import account_service
from Python_Bank_Api.Services.account_service_impl import AccountServiceImpl
import logging

from Python_Bank_Api.Views.user_routes import user_service

app: Flask = Flask(__name__)
# For logging
# logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

account_dao = AccountDaoPostgres()
# account_dao = AccountDaoLocal()
user_dao = User(0, 'jokky', 'Bas', 'mnbvc', 0)

account_service = AccountServiceImpl(account_dao, user_dao)  # Dependency injection!
"""
@app.route("/accounts", methods=["POST"])
def create_account():
    account = request.json
    print(account)
    return "test"
"""


@app.route("/accounts", methods=["POST"])
def create_account():
    body = request.json
    account = Account(0, int(body["account_no"]), body["account_name"], body["account_type"], body["address"],
                      int(body["phone_no"]), int(body["balance"]), int(body["user_id"]))
    account_service.create_account(account)
    print(account)
    return f"Created account successfully with id {account.account_id}.", 201


@app.route("/accounts/<account_id>", methods=["GET"])
def get_account_by_id(account_id: str):
    try:
        account = account_service.get_account_by_id(int(account_id))
        return jsonify(account.as_json_dict())
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/accounts", methods=["GET"])
def get_all_accounts():
    accounts = account_service.get_all_accounts()
    json_accounts = [a.as_json_dict() for a in accounts]
    return jsonify(json_accounts)
    name = request.args.get("name")
    if name is not None:
        accounts - account_service.find_account_by_name_containing(name)
        json_accounts = [a.json_deserialize() for a in accounts]
        return jsonify(json_accounts)
    else:
        accounts = account_service.get_all_accounts()
        json_accounts = [a.as_json_dict() for a in accounts]
        return jsonify(json_accounts)


@app.route("/accounts/<account_id>", methods=["PUT"])
def update_account(account_id: str):
    body = request.json
    account = Account(int(body["account_id"]), int(body["account_no"]), body["account_name"], body["account_type"],
                      body["address"], int(body["phone_no"]), int(body["balance"]), int(body["user_id"]))
    account.account_id = int(account_id)
    account_service.update_account(account)
    return "Updated successfully!"


@app.route("/accounts/<account_id>", methods=["DELETE"])
def delete_account(account_id: str):
    try:
        account_service.delete_account_by_id(int(account_id))
        return "Deleted Successfully", 200
    except ResourceNotFoundError as e:
        return "The resource could not be found", 404


@app.route("/accounts/<uid>", methods=["GET"])
def get_accounts_by_user_id(uid: str):
    try:
        if not uid.isnumeric():
            raise ValueTypeError
        accounts = account_service.get_account_by_user_id(int(uid))
        app.logger.info(f' all accounts with user_id: {uid}')
        return jsonify([account.as_json_dict() for account in accounts]), 200
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/accounts/uid/<uid>/lower/<lower>/greater/<greater>", methods=["GET"])
# @app.route("/accounts/lower/<lower>/grater/<grater>", methods=["GET"])
def get_accounts_by_user_id_and_range(uid: str, lower: str, greater: str):
    # def get_accounts_by_user_id_and_range(lower: str, grater: str):
    try:
        if not (uid.isnumeric() and lower.isnumeric() and greater.isnumeric()):
            # if not (lower.isnumeric() and grater.isnumeric()):
            raise ValueTypeError
        accounts = account_service.get_accounts_by_user_id_and_range(int(uid), int(lower), int(greater))
        app.logger.info(f' Accounts with user_id: {uid} and range between {lower} and {greater}')
        return jsonify([account.as_json_dict() for account in accounts]), 200
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/accounts/uid/<uid>/account_id/<account_id>", methods=["GET"])
def get_accounts_by_user_id_and_account_id(uid: str, account_id: str):
    try:
        if not (uid.isnumeric() and account_id.isnumeric()):
            raise ValueTypeError
        account = account_service.get_account_by_user_id_and_account_id(int(uid), int(account_id))
        app.logger.info(f' get account with user_id: {uid} and account_id: {account_id}')
        return jsonify(account.as_json_dict())
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/accounts/uid/<uid>/account_id/<account_id>", methods=["PUT"])
def update_accounts_by_user_id_and_account_id(uid: str, account_id: str):
    try:
        if not (uid.isnumeric() and account_id.isnumeric()):
            raise ValueTypeError
        account = Account.as_json_dict(request.json)
        account = account_service.update_account_by_user_id_and_account_id(account, int(uid),
                                                                           int(account_id))
        app.logger.info(f' get account with user_id: {uid} and account_id: {account_id}')
        return jsonify(account.as_json_dict())
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/accounts/uid/<uid>/account_id/<account_id>", methods=["DELETE"])
def delete_accounts_by_user_id_and_account_id(uid: str, account_id: str):
    try:
        if not (uid.isnumeric() and account_id.isnumeric()):
            raise ValueTypeError
        account_service.delete_account_by_user_id_and_account_id(int(uid), int(account_id))
        app.logger.info(f' deleted account with user_Id: {uid} and account_Id: {account_id}')
        return f'account with user_id: {uid} and account_id: {account_id}  deleted successfully'
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/accounts/uid/<uid>/account_id/<account_id>", methods=["PATCH"])
def transaction_account_by_user_id_and_account_id(uid: str, account_id: str):
    try:
        if not (uid.isnumeric() and account_id.isnumeric()):
            raise ValueTypeError
        body = request.json
        deposit = withdraw = 0
        if "deposit" in body:
            deposit = int(body["deposit"])
        if "withdraw" in body:
            withdraw = int(body["withdraw"])
        account = account_service.transaction_account_by_user_id_and_account_id(int(uid), int(account_id), withdraw,
                                                                                deposit)

        app.logger.info(
            f' transaction in  account with user_Id: {uid} and account_Id: {account_id}')
        return jsonify(account.as_json_dict())
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404
    except InsufficientFund as e:
        return str(e), 402


# def create_user_route(app: Flask):

@app.route('/users', methods=['POST'])
def post_user():
    body = request.json
    user = User(0, body["name"], body["username"], body["passwords"], int(body["account_id"]))
    # user.uid = int(account_id)

    # json = request.json
    # print(json)
    # user = User.as_json_dict(json)
    # u = User(json[])
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
        # user_service.get_user_by_id(int(uid))
        body = request.json
        user = User(0, body['name'], '', '', 0) # User.json_deserialize(request.json)
        user.uid = int(uid)
        user_service.update_user(user)
        user = user_service.get_user_by_id(int(uid))
        app.logger.info(f'User with Id:{user.uid} updated successfully')
        return jsonify(user.as_json_dict())
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404


@app.route("/user/<uid>", methods=["DELETE"])
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


@app.route("/accounts/account1_id/<account1_id>/account2_id/<account2_id>", methods=["PATCH"])
def transfer_amount_between_accounts_by_account_id(account1_id: str, account2_id: str):
    try:
        if not (account1_id.isnumeric() and account2_id.isnumeric()):
            raise ValueTypeError
        body = request.json
        amount = body["amount"]
        res = account_service.transfer_amount_between_accounts_with_account_id(int(account1_id),
                                                                               int(account2_id), int(amount))

        app.logger.info(
            f' transaction happened in  accounts with account1_Id: {account1_id} and account2_Id: {account2_id}')
        return jsonify([account.as_json_dict() for account in res])
    except ValueTypeError as e:
        return str(e), 404
    except ResourceNotFoundError as e:
        return str(e), 404
    except InsufficientFund as e:
        return str(e), 422


##############################################################################################
"""
@app.route("/accounts", methods=["POST"])
def create_account( user_id: str):
    try:
        if not type(int(user_id))
            body= request.json
            account= Account(body["account_id"], body["account_no"], body["account_name"], body["account_type"], body["address"],
                             body["phone_no"], body["balance"])
            account_service.create-account_by_user_id(account,int(user_id))
            app.logger.info("new account created with id {account.account-no}")
            return jsonify (account.as_json_dict(), 201)
           raise ResourceNotFoundError

           account.account_no= cursor.fetchone()[0]
        return account


@app.route("/accounts/deposit/<account_id>", hods=["POST"])
def deposit_to_account(account_id: str):
    try:
        account_service.deposit(int(account_id))
        return "Deleted Successfully", 200
    except ResourceNotFoundError as e:
        return "The resource could not be found", 404
"""
"""
@app.route("/accounts/withdraw/<account_id>", hods=["POST"])
def withdraw_to_account(account_id: str):
    pass

@app.route("/accounts/transfer/<account_id>", hods=["POST"])
def transfer(account_id: str):
    pass
"""
# include deposit, withdraw and transfer methods below


if __name__ == '__main__':
    app.run(debug=True)
