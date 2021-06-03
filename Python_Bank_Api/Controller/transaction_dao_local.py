from typing import List

from Python_Bank_Api.Controller.transaction_dao import TransactionDAO
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models import transactions
from Python_Bank_Api.Models.transactions import Transaction


class TransactionDaoLocal(TransactionDAO):
    id_maker = 0  # mimic a primary key generator in a database
    transaction_table = {}  # mimicing a table in a database

    def deposit(self, amount, balance) -> float:
        if amount > 0:
            self.balance += amount
            self.statement()
            return True

    def withdraw(self, amount, balance) -> float:
        if balance >= amount:
            self.balance -= amount
            self.statement()
        else:
            print("Insufficient fund")
            self.statement()

    def transfer(self, amount: float, account_no):
        self.balance = self.balance - amount
        account_no.balance = account_no.balance + amount
        return account_no.balance()

    def get_transaction_by_id(self, transaction_id: int) -> Transaction:
        transaction = TransactionDaoLocal.transaction_table.get(transaction_id)
        if transaction == None:
            raise ResourceNotFoundError
        return transaction

    def get_all_transactions(self) -> List[Transaction]:
        transaction_list = list(TransactionDaoLocal.transaction_table.values())
        return transaction_list

    def statement(self) -> str:
        print("Hi {} your current balance is {}".format(transactions.account_no, self.balance))  # check later unresolve
