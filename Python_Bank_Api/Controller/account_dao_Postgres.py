from abc import ABC
from typing import List
from psycopg2 import sql
from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.accounts import Account
from Python_Bank_Api.connection_utils import connection


class AccountDaoPostgres(AccountDAO, ABC):

    def create_account_by_account_id(self, account: Account) -> Account:
        try:
            sql = """ insert into account(account_no, account_name, account_type, address, phone_no, balance, u_id)
              values (%s, %s, %s, %s, %s, %s, %s) returning account_id """
            cursor = connection.cursor()
            cursor.execute(sql, [account.account_no, account.account_name, account.account_type, account.address, account.phone_no, account.balance, account.uid])
            connection.commit()
            account.account_id = cursor.fetchone()[0]
        except Exception as e:
            print(e)
        return account

    def get_account_by_id(self, account_id: int) -> Account:

        sql = """select * from account where account_id = %s """
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        account = Account(*record)
        return account

    def get_all_account_by_user_id(self, uid: int) -> [Account]:
        sql = """select * from account where u_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [uid])
        records = cursor.fetchall()
        accounts = [Account(*record) for record in records]
        if len(accounts) == 0:
            raise ResourceNotFoundError
        return accounts

    def get_accounts_by_user_id_and_range(self, uid: int, lower: int, grater: int) -> [Account]:
        sql = """select * from account where u_id = %s and balance between %s and %s """
        # sql = """select * from account where balance between %s and %s """
        cursor = connection.cursor()
        cursor.execute(sql, [uid, lower, grater])
        # cursor.execute(sql, [lower, grater])
        records = cursor.fetchall()
        accounts = [Account(*record) for record in records]
        if len(accounts) == 0:
            raise ResourceNotFoundError
        return accounts

    def get_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> Account:
        sql = """select * from account where u_id= %s and account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [uid, account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        account = Account(*record)
        return account

    def update_account_by_user_id_and_account_id(self, account: Account, uid: int, account_id: int) -> Account:
        sql = """update account set account_type = %s, balance = %s where account_id = %s and u_id = %s returning 
        account_id, u_id ; """
        cursor = connection.cursor()
        cursor.execute(sql, [account.account_type, account.balance, account_id, uid])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        account.account_id = record[0]
        account.uid = record[1]
        return account

    def get_all_accounts(self) -> List[Account]:
        sql = """select * from account"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        account_list = []
        for record in records:
            account_list.append(Account(*record))
        return account_list

    def delete_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> bool:
        sql = """delete from account where u_id = %s and account_id = %s returning account_id ;"""
        cursor = connection.cursor()
        cursor.execute(sql, [uid, account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        return True

    def delete__account_by_user_id(self, uid: int) -> bool:
        sql = """delete from account where u_id = %s ;"""
        cursor = connection.cursor()
        cursor.execute(sql, [uid])
        connection.commit()
        return True

    def update_account(self, account: Account) -> Account:
        sql = """update account set account_no = %s, account_name = %s, account_type = %s, address = %s, 
        phone_no = %s, balance = %s where account_id = %s AND u_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (
            account.account_no, account.account_name, account.account_type, account.address,
            account.phone_no, account.balance, account.account_id, account.uid))
        connection.commit()
        return account

    def delete_account_by_id(self, account_id: int) -> bool:
        sql = """delete from account where account_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
        return True

    def update_account_balance_by_account_id(self, balance: int, account_id: int):
        sql = """update account set balance = %s where account_id = %s returning account_id;"""
        cursor = connection.cursor()
        cursor.execute(sql, [balance, account_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        return True
