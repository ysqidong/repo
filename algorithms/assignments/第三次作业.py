class Multipledict:
    def __init__(self,size: int = 100):
        """哈希表
        时间复杂度：O(1)
        returns: dict
        """
        self.size = size
        self.table = [None] * self.size
    def hash_function(self, key: str) -> int:
        return sum(ord(char) for char in key) % self.size
    def insert(self, key: str, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    self.table[index][i] = (key, value)
                    return
            self.table[index].append((key, value))
    def search(self, key: str):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None
