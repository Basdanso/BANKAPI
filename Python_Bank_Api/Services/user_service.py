from abc import ABC, abstractmethod
from typing import List

from Python_Bank_Api.Models.accounts import Account
from Python_Bank_Api.Models.users import User


class UserServices(ABC):
    @abstractmethod
    def create_user(self, name: str, username: str, passwords: str) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, uid: int) -> User:
        pass

    @abstractmethod
    def get_user_by_name(self, name: str) -> List[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, account: User) -> User:
        pass

    @abstractmethod
    def delete_user_by_id(self, uid: int) -> bool:
        pass
