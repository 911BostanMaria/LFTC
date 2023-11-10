class SymbolTable:
    def __init__(self, size):
        self.identifier_table = HashTable(size)
        self.constant_table = HashTable(size)

    def add_identifier(self, name):
        return self.identifier_table.add(name,None)

    def add_constant(self, constant):
        return self.constant_table.add(constant, None)

    def has_identifier(self, name):
        return self.identifier_table.contains(name)

    def has_constant(self, constant):
        return self.constant_table.contains(constant)

    def get_position_identifier(self, name):
        return self.identifier_table.get_position(name)

    def get_position_constant(self, constant):
        return self.constant_table.get_position(constant)

    def to_string(self):
        identifier_str = "Identifier Table:\n" + self.identifier_table.to_string()
        constant_str = "Constant Table:\n" + self.constant_table.to_string()
        return identifier_str + "\n" + constant_str

class HashTable:
    """
    Separate Chaining:
     In separate chaining, each bucket (index) in the hash table maintains a list (or another data structure like a linked list)
     of key-value pairs that hash to the same index. When a collision occurs, the new key-value pair is appended to this list.
    """
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash(self, key):
        if isinstance(key, str):
            sum_ascii = sum(ord(char) for char in key)
            return sum_ascii % self.size
        elif isinstance(key, int):
            return key % self.size

    def get_size(self):
        return self.size

    def get_hash_value(self, key):
        return self.hash(key)

    def add(self, key, value):
        index = self.hash(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i, (existing_key, _) in enumerate(self.table[index]):
                if existing_key == key:
                    return -1
            self.table[index].append((key, value))

    def get(self, key):
        index = self.hash(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        raise KeyError("Key not found in the table")

    def contains(self, key):
        index = self.hash(key)
        if self.table[index] is not None:
            for k, _ in self.table[index]:
                if k == key:
                    return True
        return False

    def get_position(self, key):
        index = self.hash(key)
        if self.contains(key):
            return index
        else:
            return -1

    def to_string(self):
        result = ""
        for i in range(self.size):
            if self.table[i]:
                result += f'{i} -> {str(self.table[i])}\n'
        return result

