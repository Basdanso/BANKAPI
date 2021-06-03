from abc import ABC, abstractmethod
from typing import List

from Python_Bank_Api.Models.accounts import Account


class AccountServices(ABC):
    @abstractmethod
    def create_account(self, account: Account):
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int):
        pass

    @abstractmethod
    def get_account_by_name(self, name: str) -> List[Account]:
        pass

    def find_account_by_name_containing(self, phrase: str) -> List[Account]:
        pass

    @abstractmethod
    def get_all_accounts(self):
        pass

    @abstractmethod
    def update_account(self, account: Account):
        pass

    @abstractmethod
    def delete_account_by_id(self, account_id: int):
        pass

    @abstractmethod
    def create_account_by_user_id(self, account: Account, customer_id: int) -> Account:
        pass

    @abstractmethod
    def get_account_by_user_id(self, uidid: int) -> list[Account]:
        pass

    @abstractmethod
    def get_accounts_by_user_id_and_range(self, uid: int, lower: int, grater: int) -> [Account]:
        pass

    @abstractmethod
    def get_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def update_account_by_user_id_and_account_id(self, account: Account, customer_id: int, account_id: int) -> Account:
        pass

    @abstractmethod
    def delete_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> bool:
        pass

    @abstractmethod
    def delete_account_by_user_id(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def transaction_account_by_user_id_and_account_id(self, customer_id: int, account_id: int, withdraw: int,
                                                      deposit: int) -> Account:
        pass

    @abstractmethod
    def transfer_amount_between_accounts_with_account_id(self, account1_id: int, account2_id: int, amount: int) -> [
        Account]:
        pass

    @staticmethod
    def statement(self):
        pass
