class Transaction:
    def __init__(self, num, tuple_id, column, old_v):
        self.num      = num
        self.tuple_id = tuple_id
        self.column   = column
        self.old_v    = old_v

    def __str__(self):
        return f"<{self.num}|{self.tuple_id}|{self.column}|{self.old_v}>"