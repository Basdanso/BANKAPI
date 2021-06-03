from unittest import TestCase

from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Controller.account_dao_Postgres import AccountDaoPostgres
from Python_Bank_Api.Controller.account_dao_local import AccountDaoLocal
from Python_Bank_Api.Models.accounts import Account, account

account_dao = AccountDaoPostgres()
#account_dao = AccountDaoLocal()

test_account = Account(0, 101, "Bas", "Current", "New York", 4321, 2000)


def test_create_account():
    account_dao.create_account_by_account_id(test_account)
    assert test_account.account_id != 0

def test_get_account_by_id():
    account = account_dao.get_account_by_id(test_account.account_id)
    TestCase().assertDictEqual(account.as_json_dict(), test_account.as_json_dict())


def test_update_account():
    test_account.available = True
    update_account = account_dao.update_account(test_account)
    assert update_account.account_id == test_account.account_id


def test_delete_account():
    result = account_dao.delete_account_by_id(test_account.account_id)
    assert result == True


def test_get_all_accounts():
    account1 = Account(0, 101, "Bas", "Current", "New York", 4321, 500)
    account2 = Account(0, 102, "Adam", "Current","WVA", 7112, 1000)
    account_dao.create_account_by_account_id(account1)
    account_dao.create_account_by_account_id(account2)
    account = account_dao.get_all_accounts()
    assert len(account) >= 2