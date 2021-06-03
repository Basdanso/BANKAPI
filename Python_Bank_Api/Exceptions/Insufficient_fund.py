class InsufficientFund(Exception):
    description: str = 'Occurs when there is not enough budget.'

    def __str__(self):
        return "Insufficient Fund"