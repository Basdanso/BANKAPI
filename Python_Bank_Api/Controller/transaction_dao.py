from abc import ABC, abstractmethod
from typing import List

from Python_Bank_Api.Models.transactions import Transaction


class TransactionDAO(ABC):

    @abstractmethod
    def deposit(self, amount: float, balance: float) -> Transaction:
        pass

    @abstractmethod
    def withdraw(self, amount: float, balance: float) -> Transaction:
        pass

    @abstractmethod
    def transfer(self, amount: float, account_no):
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        pass

    @abstractmethod
    def get_all_transactions(self) -> List[Transaction]:
        pass

    @abstractmethod
    def statement(self) -> str:
        pass




