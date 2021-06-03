class Account:

    def __init__(self, account_id: int, account_no: int, account_name: str,
                 account_type: str, address: str, phone_no: int, balance=0, uid=0):
        self.account_id = account_id
        self.account_no = account_no
        self.account_name = account_name
        self.account_type = account_type
        self.address = address
        self.phone_no = phone_no
        self.balance = balance
        self.uid = uid

    def __str__(self):
        return f" id= {self.account_id}, account_no= {self.account_no}, name= {self.account_name}, " \
               f"account_type: {self.account_type}, address: {self.address}," \
               f" phone_no: {self.phone_no}, balance: {self.balance}, uid: {self.uid}"

    def as_json_dict(self):
        return {
            "accountId": self.account_id,
            "accountNo": self.account_no,
            "accountName": self.account_name,
            "accountType": self.account_type,
            "address": self.address,
            "phoneNo": self.phone_no,
            "balance": self.balance,
            "uid": self.uid,
        }


account = Account(0, 101, 'Basiru', 'Current', 'New york', 1234, 200, 1)
#print(account)
#print(Account.counter)
