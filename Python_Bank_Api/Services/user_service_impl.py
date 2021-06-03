from typing import List

from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Models import users
from Python_Bank_Api.Models.users import User
from Python_Bank_Api.Services.user_service import UserServices


class UserServiceImpl(UserServices):
    def __init__(self, user_dao: UserDAO):
        self.user_dao= user_dao

    def create_user(self, user: User) -> User:
        return self.user_dao.create_user(user)

    def get_user_by_id(self, uid: int) -> User:
        return self.user_dao.get_user_by_id(uid)

    def get_user_by_name(self, name: str) -> List[User]:
        users = self.get_all_users()
        return [user for user in users if name.lower() in user.names.lower()]

    def get_all_users(self) -> List[User]:
        return self.user_dao.get_all_users()

    def update_user(self, user: User) -> User:
        return self.user_dao.update_user(user)

    def delete_user_by_id(self, uid: int) -> bool:
        self.user_dao.get_user_by_id(uid)
        self.user_dao.delete_user_by_id(uid)
        return True









