from abc import abstractmethod, ABC
from typing import List

from Python_Bank_Api.Models.accounts import Account


class AccountDAO(ABC):

    @abstractmethod
    def create_account_by_account_id(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> List[Account]:
        pass

    @abstractmethod
    def update_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def delete_account_by_id(self, account_id: int) -> bool:
        pass

    @abstractmethod
    def update_account_balance_by_account_id(self, balance: int, account_id: int):
        pass

    @abstractmethod
    def delete__account_by_user_id(self, uid: int) -> bool:
        pass

    @abstractmethod
    def delete_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def update_account_by_user_id_and_account_id(self, account: Account, uid: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_accounts_by_user_id_and_range(self, uid: int, lower: int, grater: int) -> [Account]:
        pass

    @abstractmethod
    def get_all_account_by_user_id(self, uid: int) -> [Account]:
        pass

    @abstractmethod
    def create_account_by_account_id(self, account: Account, user_id: int) -> Account:
        pass


