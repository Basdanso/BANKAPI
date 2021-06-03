from typing import List

from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.users import User


class UserDaoLocal(UserDAO):
    id_maker = 0  # mimic a primary key generator in a database
    user_table = {}  # mimicing a table in a database

    def create_user(self, user: User) -> User:
        UserDaoLocal.id_maker += 1
        UserDaoLocal.user_table[UserDaoLocal.id_maker] = user
        user.uid = UserDaoLocal.id_maker
        return user

    def get_user_by_id(self, uid: int) -> User:
        try:
            user = UserDaoLocal.user_table.get(uid)
            return user
        except KeyError:
            raise ResourceNotFoundError(f"Could not find user of id {uid}")

    def get_all_users(self) -> List[User]:
        user_list = list(UserDaoLocal.user_table.values())
        return user_list

    def update_user(self, uid: int) -> User:
        try:
            user = UserDaoLocal.user_table[uid]
            return user
        except KeyError:
            raise ResourceNotFoundError(f"User not find user with id {uid}")

    def delete_user_by_id(self, uid: int) -> bool:
        try:
            del UserDaoLocal.user_table[uid]
            return True
        except KeyError:
            raise ResourceNotFoundError(f"User with id {uid} not found")

