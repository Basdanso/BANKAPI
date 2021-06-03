from abc import ABC
from typing import List

from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.accounts import Account, account


class AccountDaoLocal(AccountDAO):

    id_maker = 0  # mimic a primary key generator in a database
    account_table = {}  # mimicing a table in a database

    def create_account(self, account: Account) -> Account:
        AccountDaoLocal.id_maker += 1
        account.account_id = AccountDaoLocal.id_maker
        # adding a new item to a dictionary
        AccountDaoLocal.account_table[AccountDaoLocal.id_maker] = account
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        account = AccountDaoLocal.account_table.get(account_id)
        if account == None:
            raise ResourceNotFoundError
        return account

    def get_all_accounts(self) -> List[Account]:
        account_list = list(AccountDaoLocal.account_table.values())
        return account_list

    def update_account(self, account: Account) -> Account:
        AccountDaoLocal.account_table[account.account_id] =account
        return account

    def delete_account_by_id(self, account_id: int) -> bool:
        try:
            AccountDaoLocal.account_table.pop(account_id)
            return True
        except KeyError:
            return False