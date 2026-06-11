class BubbleSort:
    def __init__(self, arr: list[int|float]):
        """冒泡排序算法
        时间复杂度：O(n^2)
        returns: list[int|float]
        """
        self.arr = arr
        self.n = len(arr)
    def sort(self):
        n = len(self.arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
        return self.arr
#选择排序
class SelectionSort:
    def __init__(self, arr: list[int|float]):
        """选择排序算法
        时间复杂度：O(n^2)
        returns: list[int|float]
        """
        self.arr = arr
        self.n = len(arr)
    def sort(self):
        n = len(self.arr)
        for i in range(n):
            min_idx = i
            min_value = self.arr[i]
            for j in range(i + 1, n):
                if self.arr[j] < self.arr[min_idx]:
                    min_idx = j
                    min_value = self.arr[j]
            self.arr[i], self.arr[min_idx] = self.arr[min_idx], self.arr[i]
        return self.arr
#插入排序
class InsertionSort:
    def __init__(self, arr: list[int|float]):
        """插入排序算法
        时间复杂度：O(n^2)
        returns: list[int|float]
        """
        self.arr = arr
        self.n = len(arr)
    def sort(self)-> list[int|float]:
        n = len(self.arr)
        for index in range(1, n):
            position = index
            temp_value = self.arr[index]
            while position > 0 and self.arr[position - 1] > temp_value:
                self.arr[position] = self.arr[position - 1]
                position -= 1
            self.arr[position] = temp_value
        return self.arr
#哈希表
class Multipledict:
    def __init__(self,size: int = 100):
        """哈希表
        时间复杂度：O(1)
        returns: dict
        """
        self.size = size
        self.table:list[list[tuple[str,int]]] = [[] for _ in range(size)]
    def calc_multiple_result(self, key, value)->int:
        """计算键的乘积"""
        for char in key:
            value *= ord(char)- ord('a') + 1
            value%= self.size#取模，防止溢出
        return value
    def insert(self, key: str, value: int):
        """插入键值对"""
        index = self.calc_multiple_result(key, value)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))
    def search(self, key: str) -> int|None:
        """搜索键对应的值"""
        index = self.calc_multiple_result(key, 1)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None
    def delete(self, key: str):
        """删除键值对"""
        index = self.calc_multiple_result(key, 1)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return