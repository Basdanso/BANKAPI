from abc import ABC, abstractmethod

from Python_Bank_Api.Models.transactions import Transaction


class TransactionServices(ABC):

    @abstractmethod
    def deposit(self, transaction: Transaction):
        pass

    @abstractmethod
    def withdraw(self, account_id: int):
        pass

    @abstractmethod
    def transfer(self, name: str):
        pass