from Python_Bank_Api.Controller.user_dao_local import UserDaoLocal
from Python_Bank_Api.Controller.user_dao_postgres import UserDaoPostgres
from Python_Bank_Api.Exceptions.not_found_exception import ResourceNotFoundError
from Python_Bank_Api.Models.users import user, User
from unittest import TestCase

#user_dao = UserDaoLocal()
user_dao = UserDaoPostgres()

test_user = User(0, "Sam", "sam123", "password", 1)


def test_create_user():
    result = user_dao.create_user(test_user)
    assert result.uid > 0


def test_get_user_by_id():
    uid = user_dao.create_user(test_user)
    result = user_dao.get_user_by_id(uid.uid)
    TestCase().assertDictEqual(result.as_json_dict(), uid.as_json_dict())


def test_get_user_by_id_invaild():
    try:
        user_dao.get_user_by_id(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_update_user():
    user = user_dao.create_user(test_user)
    user.username = "updated"
    update_user = user_dao.update_user(user)
    assert update_user.username == user.username


def test_update_user_invalid():
    try:
        user_dao.update_user(User(-1, "", "", "", 1))
        assert False
    except ResourceNotFoundError:
        assert True


def test_delete_user_by_id():
    user = user_dao.create_user(test_user)
    assert user_dao.delete_user_by_id(user.uid)
    try:
        user_dao.get_user_by_id(user.uid)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_all_users():
    user1 = User(0, "Bas", "bas@revature", "password123", 1)
    user2 = User(0, "Adam", "adam@revature", "passwordABC", 1)
    user_dao.create_user(user1)
    user_dao.create_user(user2)
    user = user_dao.get_all_users()
    assert len(user) >= 1