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
class SimpleOrderedSet:
    """一个简单的有序集合类，支持插入和显示操作"""
    def __init__(self):
        self.data = [0] * 100  # 假设最大容量为100
        self.size = 0
    def insert(self, x):
        """将x插入有序集合（保持升序）"""
      
        
        # 检查是否重复
        for i in range(self.size):
            if self.data[i] == x:
                print(f"{x} 已存在")
                return False
        
        #  找到插入位置
        pos = self.size  # 默认插到最后
        for i in range(self.size):
            if self.data[i] > x:
                pos = i
                break
        
        #从后往前移动元素
        
        for i in range(self.size, pos, -1):
            self.data[i] = self.data[i-1]
        
        # 插入新元素
        self.data[pos] = x
        self.size += 1
        
        print(f"插入 {x} 成功")
        return True
    
    def show(self):
        """显示集合"""
        print(self.data[:self.size])
# 测试代码
if __name__ == "__main__":
    ordered_set = SimpleOrderedSet()
    ordered_set.insert(5)
    ordered_set.insert(3)
    ordered_set.insert(8)
    ordered_set.show()  # 输出: [3, 5, 8]