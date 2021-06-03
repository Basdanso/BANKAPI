from typing import List
from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.users import User
from Python_Bank_Api.connection_utils import connection


class UserDaoPostgres(UserDAO):

    def create_user(self, user: User) -> User:
        sql = """insert into users (name,username,passwords,account_id) values (%s,%s,%s,%s) returning user_id """
        cursor = connection.cursor()
        cursor.execute(sql, [user.name, user.username, user.passwords, user.account_id])
        connection.commit()
        user.uid = cursor.fetchone()[0]
        return user

    def get_user_by_id(self, uid: int) -> User:
        sql = """select * from users where user_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [uid])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError
        else:
            user = User(*record)
        return user

    def get_all_users(self) -> [User]:
        sql = """select * from users"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        users = [User(*record) for record in records]
        if len(users) == 0:
            raise ResourceNotFoundError("No user with records found")
        else:
            return users

    def update_user(self, user: User) -> User:
        sql = """update users set name=%s where user_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [user.name, user.uid])
        connection.commit()
        return user

    def delete_user_by_id(self, uid: int) -> bool:
        sql = """delete from users where user_id =%s"""
        cursor = connection.cursor()
        cursor.execute(sql, [uid])
        connection.commit()
        return True