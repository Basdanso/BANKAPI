from Python_Bank_Api.Models.accounts import Account, account


class User:
    counter = 0

    def __init__(self, uid: int, name: str, username: str, passwords: str, account_id: int):
        self.uid = uid
        self.name = name
        self.username = username
        self.passwords = passwords
        self.account_id = account_id
        User.counter += 1

    def __str__(self):
        return f"Uid={self.uid}, Name={self.name}, Username={self.username}, Passwords={self.passwords}, AccountId={self.account_id}"

    def as_json_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'username': self.username,
            'password': self.passwords,
            'account_id': self.account_id,
        }

    @staticmethod
    def json_deserialize(json):
        user = User(0, '', '', '', 0)
        # user.uid = json['uid']
        account.account_name = ['name']
        user.username = json['username']
        user.password = json['password']
        user.account_id = json['account_id']
        return user


user = User(0, 'jokky', 'Bas', 'mnbvc', 0)
print(user)
