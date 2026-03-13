class SimpleSet:
    """一个简单的集合类，支持插入、删除和查询操作"""
    def __init__(self):
        self.elements = []

    def insert(self, value):
        """插入元素，若已存在则不重复插入"""
        for i in range(len(self.elements)):
            if self.elements[i] == value:
                return
        self.elements.append(value)

    def delete(self, value):
        """删除元素，若不存在则不做操作"""
        for i in range(len(self.elements)):
            if self.elements[i] == value:
                self.elements.pop(i)
                return

    def query(self, value):
        """查询元素是否存在"""
        return value in self.elements

    def __str__(self):
        return str(self.elements)
# 测试代码
if __name__ == "__main__":
    my_set = SimpleSet()
    my_set.insert(1)
    my_set.insert(2)
    my_set.insert(3)
    print(my_set)  # 输出: [1, 2, 3]
    print(my_set.query(2))  # 输出: True
    my_set.delete(2)
    print(my_set)  # 输出: [1, 3]
    print(my_set.query(2))  # 输出: False
def insert_into_sorted_array(arr, value):
    """
    将 value 插入有序数组 arr，保持升序，假设 arr 无重复
    返回插入后的新数组
    """
    if value>arr[len(arr)-1]:
        arr.append(value)
        return arr
    if value<arr[0]:
        arr.insert(0, value)
        return arr
    # 找到第一个大于等于 value 的位置
    i = 0
    while i < len(arr) and arr[i] < value:
        i += 1
    # 插入
    arr.insert(i, value)
    return arr
# 测试代码
if __name__ == "__main__":
    arr = [1, 3, 5, 7]
    print(insert_into_sorted_array(arr, 4))  # 输出: [1, 3, 4, 5, 7]
    print(insert_into_sorted_array(arr, 0))  # 输出: [0, 1, 3, 4, 5, 7]
    print(insert_into_sorted_array(arr, 8))  # 输出: [0, 1, 3, 4, 5, 7, 8]