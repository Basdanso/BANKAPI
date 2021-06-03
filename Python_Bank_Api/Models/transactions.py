
class Transaction:

    counter = 0

    def __init__(self, transaction_id: int, account_no: int, amount: int, balance: int, timestamp: str):
        self.transaction_id = transaction_id
        self.account_no = account_no
        self.amount = amount
        self.balance = balance
        self.timestamp = timestamp
        Transaction.counter += 1

    def __str__(self):
        return f"Transaction: {self.transaction_id}, Account_Id: {self.account_no}" \
               f"Amount: {self.amount}, Balance: {self.balance}, Timestamp: {self.timestamp}"

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

    def statement(self):
        print("Hi {} your current balance is {}".format(self.account_no,self.balance))

    def transfer(self, amount, account_no):
        self.balance = self.balance - amount
        account_no.balance = account_no.balance + amount
        return account_no.balance()


    def json(self):
        return{
            'transaction_id' : self.transaction_id,
            'account_no': self.account_no,
            'amount': self.amount,
            'balance': self.balance

        }
    @staticmethod
    def json_deserialize(json):
        transaction = Transaction(0, 0, 0,0)
        transaction.transaction_id = json["transactionId"]
        transaction.account_no = json['account_no']
        transaction.amount = json['amount']
        transaction.balance = json['balance']
        return transaction

