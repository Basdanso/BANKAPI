from typing import List

from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Exceptions.Insufficient_fund import InsufficientFund
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models import accounts
from Python_Bank_Api.Models.accounts import Account
from Python_Bank_Api.Services.account_service import AccountServices


class AccountServiceImpl(AccountServices):

    def __init__(self, account_dao: AccountDAO, user_dao: UserDAO):
        self.account_dao = account_dao
        self.user_dao = user_dao

    def create_account_by_user_id(self, account: Account, u_id: int) -> Account:
        self.user_dao.get_user_by_id(u_id)
        account.u_id = u_id
        return self.account_dao.create_account(account)

    def get_account_by_user_id(self, uid: int) -> list[Account]:
        self.user_dao.get_user_by_id(uid)
        return self.account_dao.get_all_account_by_user_id(uid)

    def get_accounts_by_user_id_and_range(self, uid: int, lower: int, grater: int) -> [Account]:
        # self.user_dao.get_user_by_id(uid)
        return self.account_dao.get_accounts_by_user_id_and_range(uid, lower, grater)

    def get_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> Account:
        return self.account_dao.get_account_by_user_id_and_account_id(uid, account_id)

    def update_account_by_user_id_and_account_id(self, account: Account, user_id: int, account_id: int) -> Account:
        return self.account_dao.update_account_by_user_id_and_account_id(account, user_id, account_id)

    def delete_account_by_user_id_and_account_id(self, uid: int, account_id: int) -> bool:
        self.account_dao.delete_account_by_user_id_and_account_id(uid, account_id)

    def delete_account_by_user_id(self, uid: int) -> bool:
        self.account_dao.delete__account_by_user_id(uid)

    def transaction_account_by_user_id_and_account_id(self, uid: int, account_id: int, withdraw: int, deposit: int) -> Account:
        account = self.account_dao.get_account_by_user_id_and_account_id(uid, account_id)
        if account.balance < (withdraw - deposit):
            raise InsufficientFund
        account.balance += (deposit - withdraw)
        return self.account_dao.update_account_by_user_id_and_account_id(account,uid, account_id)

    def transfer_amount_between_accounts_with_account_id(self, account1_id: int, account2_id: int, amount: int) -> [
        Account]:
        account1 = self.account_dao.get_account_by_id(account1_id)
        account2 = self.account_dao.get_account_by_id(account2_id)
        if account1.balance < amount:
            raise InsufficientFund
        account1.balance -= amount
        account2.balance += amount
        self.account_dao.update_account_by_user_id_and_account_id(account1, account1.uid, account1_id)
        self.account_dao.update_account_balance_by_account_id(account2.balance, account2_id)
        return [account1, account2]

    def create_account(self, account: Account) -> Account:
        return self.account_dao.create_account_by_account_id(account)

    def get_account_by_id(self, account_id: int):
        return self.account_dao.get_account_by_id(account_id)

    def get_account_by_name(self, name: str) -> List[Account]:
        accounts = self.get_all_accounts()
        return [account for account in accounts if name.lower() in account.names.lower()]

    def get_all_accounts(self):
        return self.account_dao.get_all_accounts()

    def update_account(self, account: Account):
        return self.account_dao.update_account(account)

    def delete_account_by_id(self, account_id: int):
        result = self.account_dao.delete_account_by_id(account_id)
        if result:
            return result
        else:
            raise ResourceNotFoundError(f"account with the id of {account_id} could not be found")

    def find_account_by_name_containing(self, phrase: str) -> List[Account]:
        accounts = self.account_dao.get_all_accounts()
        filtered_accounts = []

        for account in accounts:
            if phrase in account.account_name:
                filtered_accounts.append(account)

        return filtered_accounts
########################################################################################################################
    # REVIEW THE FOLLOWING
"""
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.statement()

    def withdrawal(self, amount):
        if amount > 0 and self.balance > amount:
            self.balance -= amount
            self.statement()
        else:
            print("Insufficient fund")
            self.statement()

    def transfer(self, amount, account_no):
        self.balance = self.balance - amount
        account_no.balance = account_no.balance + amount
        return account_no.balance()

    def statement(self):
        print("Hi {} your current balance is {}".format(self.account_no,self.balance))



"""
"""
def DepositAmt():
    amount = input("Enter the amount you want to deposit: ")
    ac = input("Enter Account No: ")
    a = 'select balance from account where AccNo=%s'
    data = (ac,)
    x = db.cursor()
    x.execute(a, data)
    result = x.fetchone()
    t = result[0] + amount
    sql = ('update amount set balance where AccNo=%s')
    d = (t, ac)
    x.execute(sql, d)
    db.commit()
    main()


def WithdrawAmt():
    amount = input("Enter the amount you want to withdraw: ")
    ac = input("Enter Account No: ")
    a = 'select balance from account where AccNo=%s'
    data = (ac,)
    x = db.cursor()
    x.execute(a, data)
    result = x.fetchone()
    t = result[0] - amount
    sql = ('update amount set balance where AccNo=%s')
    d = (t, ac)
    x.execute(sql, d)
    db.commit()
    main()


def BalEnq():
    ac = input("Enter the account No: ")
    a = 'select * from amount where AccNo=%s'
    data = (ac,)
    x = db.cursor()
    x.execute(a, data)
    result = x.fetchone()
    print("Balance for account:", ac, "is", result[-1])
    main()


def DisDetails():
    ac = input("Enter the account No: ")
    a = 'select * from account where AccNo=%s'
    data = (ac,)
    x = db.cursor()
    x.execute(a, data)
    result = x.fetchone()
    for i in result:
        print(i)
    main()


def CloseAcc():
    ac = input("Enter the account No: ")
    sql1 = 'delete from account where AccNo=%s'
    sql2 = 'delete from amount where AccNo=%s'
    data = (ac,)
    x = db.cursor()
    x.execute(sql1, data)
    x.execute(sql2, data)
    db.commit()
    main()

"""

