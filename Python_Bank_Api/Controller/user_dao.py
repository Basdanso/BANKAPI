from abc import ABC, abstractmethod
from typing import List

from Python_Bank_Api.Models.users import User


class UserDAO(ABC):

    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, uid: int) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> bool:
        pass