from flask import Flask, request, jsonify

from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Controller.account_dao_Postgres import AccountDaoPostgres
from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Controller.user_dao_postgres import UserDaoPostgres
from Python_Bank_Api.Exceptions.Insufficient_fund import InsufficientFund
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Exceptions.value_type_error import ValueTypeError
from Python_Bank_Api.Models.accounts import Account
from flask import current_app as app
from Python_Bank_Api.Services.account_service import AccountServices
from Python_Bank_Api.Services.account_service_impl import AccountServiceImpl


user_dao: UserDAO = UserDaoPostgres()
account_dao: AccountDAO = AccountDaoPostgres()
account_service: AccountServices = AccountServiceImpl(account_dao, user_dao)


def create_account_route(app: Flask):
    @app.route("/accounts/<uid>", methods=["POST"])
    def post_account(uid: str):
        try:
            if not uid.isnumeric():
                raise TypeError(" The type of variable does not match.")
            account = Account.as_json_dict(request.json)
            account_service.create_account_by_user_id(account, int(uid))
            app.logger.info(f'new account registered with ID: {account.account_id}')
            return jsonify(account.serialized()), 201
        except TypeError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return str(e), 404


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


@app.route("/accounts/uid:/<uid>/lower:/<lower>/grater:/<grater>", methods=["GET"])
def get_accounts_by_user_id_and_range(uid: str, lower: str, grater: str):
    try:
        if not (uid.isnumeric() and lower.isnumeric() and grater.isnumeric()):
            raise ValueTypeError
        accounts = account_service.get_accounts_by_user_id_and_range(int(uid), int(lower), int(grater))
        app.logger.info(f' Accounts with user_id: {uid} and range between {lower} and {grater}')
        return jsonify([account.serialized() for account in accounts]), 200
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
