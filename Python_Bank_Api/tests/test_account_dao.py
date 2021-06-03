from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Controller.account_dao_Postgres import AccountDaoPostgres
from Python_Bank_Api.Controller.account_dao_local import AccountDaoLocal
from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Controller.user_dao_postgres import UserDaoPostgres
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.accounts import Account, account
from Python_Bank_Api.Models.users import User

user_dao: UserDAO = UserDaoPostgres()
account_dao: AccountDAO = AccountDaoPostgres()

test_account = Account(1, 101, "Jamas", "Current", "New York", 4321, 2000)
test_user: User = User(0, "Janie", "jane", "ASD", 1)
user_dao.create_user(test_user)



def test_create_account():
    test_account.uid = test_user.uid
    account_dao.create_account_by_account_id(test_account)
    assert test_account.account_id != 0

def test_get_all_account_by_user_id():
    test_accounts = account_dao.get_all_account_by_user_id(test_user.uid)
    assert len(test_accounts) == 1

def test_get_all_account_by_user_id_1():
    try:
        account_dao.get_all_account_by_user_id(-10)
        assert False
    except ResourceNotFoundError:
        pass

def test_get_accounts_by_user_id_and_range():
    test_accounts = account_dao.get_accounts_by_user_id_and_range(test_user.uid, 0, 1000)
    assert len(test_accounts) == 1

def test_get_accounts_by_user_id_and_range_1():
    try:
        test_accounts = account_dao.get_accounts_by_user_id_and_range(0, 0, 1000)
        assert False
    except ResourceNotFoundError:
        pass

def test_get_account_by_user_id_and_bank_account_id():
    test_account = account_dao.get_account_by_user_id_and_account_id(test_user.uid, test_user.account_id)
    assert test_account.balance == test_account.balance

def test_get_bank_account_by_customer_id_and_bank_account_id():
    try:
        account_dao.get_account_by_user_id_and_account_id(0, test_account.account_id)
        assert False
    except ResourceNotFoundError:
        pass

def test_update_account_by_user_id_and_account_id():
    test_account_new = account_dao.update_account_by_user_id_and_account_id(test_account, test_user.uid, test_account.account_id)
    assert test_account_new.balance == test_account.balance

def test_update_account_by_user_id_and_account_id_1():
    try:
        account_dao.update_account_by_user_id_and_account_id(test_account,
                                                                                test_user.uid, 0)
        assert False
    except ResourceNotFoundError:
        pass

def test_get_account_by_account_id():
    test_account_new = account_dao.get_account_by_id(test_account.account_id)
    assert test_account_new.balance == test_account.balance

def test_update_balance_bank_account_by_bank_account_id():
    account_dao.update_account_balance_by_account_id(test_account.balance,
                                                                    test_account.account_id)
    assert True

def test_delete_account_by_user_id_and_account_id():
    account_dao.delete__account_by_user_id(test_account.uid)
    assert True


####################################################################################################################
def test_get_account_by_id():
    account = account_dao.get_account_by_id(test_account.account_id)
    assert test_account.account_no == account.account_no


def test_update_account():
    test_account.available = True
    update_account = account_dao.update_account(test_account)
    assert update_account.available == test_account.available


def test_delete_account():
    result = account_dao.delete_account_by_id(test_account.account_id)
    assert result == True


def test_get_all_accounts():
    account1 = Account(0, 101, "Bas", "Current", "New York", 4321, 500)
    account2 = Account(0, 102, "Adam", "Current", "WVA", 7112, 1000)
    account_dao.create_account_by_account_id(account1)
    account_dao.create_account_by_account_id(account2)
    account = account_dao.get_all_accounts()
    assert len(account) >= 2
