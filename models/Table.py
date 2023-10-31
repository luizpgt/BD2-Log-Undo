class Table:
    def __init__(self, keys, key_types, values):
        self.keys = keys
        self.key_types = key_types 
        self.values = values

    def __str__(self):
        return f"<{self.keys}|\n{self.key_types}|\n{self.values}>"
