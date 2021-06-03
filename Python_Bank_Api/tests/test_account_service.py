#Mocking is a very common testing practice
# Faking the output of a function with predifined values
#allows us to write tests in a consistent fashion without worrying if the underlying works correctly
from unittest.mock import MagicMock

from Python_Bank_Api.Controller.account_dao import AccountDAO
from Python_Bank_Api.Controller.account_dao_Postgres import AccountDaoPostgres
from Python_Bank_Api.Controller.user_dao import UserDAO
from Python_Bank_Api.Controller.user_dao_postgres import UserDaoPostgres
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.accounts import Account, account
from Python_Bank_Api.Models.users import User
from Python_Bank_Api.Services.account_service import AccountServices
from Python_Bank_Api.Services.account_service_impl import AccountServiceImpl

account = [Account(0, 101, 'Jenny', 'Current', 'NY', 98765, 500),
           Account(0, 102, 'Mark', 'Savings', 'WVA', 5432, 1000)]

user_dao: UserDAO = UserDaoPostgres()
account_dao: AccountDAO = AccountDaoPostgres()

account_service: AccountServices = AccountServiceImpl(account_dao, user_dao)
test_user: User = User(0, "Mark", "mark1", "ABC12", 1)
user_dao.create_user(test_user)
test_account: Account = Account(0, 102, "Lolly","saving","NY", 6543, 1000)
account_dao.create_account_by_account_id(test_account)
account_dao.get_account_by_user_id_and_account_id = MagicMock(return_value=test_account)


class TestBankAccountService:
    def test_transaction_account_by_user_id_and_account_id(self):
        account = account_service.transaction_account_by_user_id_and_account_id(test_account.uid,
                                                                                         test_account.account_id,
                                                                                         0, 1000)
        assert account.balance == test_account.balance

    def test_transaction_account_by_user_id_and_account_id_1(self):
        try:
            account_service.transaction_account_by_user_id_and_account_id(0, test_account.account_id, 0,
                                                                                   1000)

            assert False
        except ResourceNotFoundError:
            pass

    def test_transfer_amount_between_accounts_with_account_id(self):
        account1 = account_dao.create_account_by_account_id(test_account)
        account2 = account_dao.create_account_by_account_id(test_account)
        print(account1)
        print(account2)
        accounts = account_service.transfer_amount_between_accounts_with_account_id(account1.account_id,
                                                                                         account2.account_id,
                                                                                         10)
        assert (accounts[1].balance - account1.balance) == 10

    def test_transfer_amount_between_accounts_with_account_id_1(self):
        try:
            account_service.transfer_amount_between_accounts_with_account_id(0, test_account.account_id,
                                                                                  1000)

            assert False
        except ResourceNotFoundError:
            pass



