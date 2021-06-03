class ValueTypeError(Exception):
    description: str = 'Occurs when type does not match'

    def __str__(self):
        return "Value type does not match"