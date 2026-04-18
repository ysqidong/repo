class Node:
    """链表节点类"""
    def __init__(self, data):
        self.data = data  # 节点数据
        self.next = None  # 指向下一个节点

class LinkedList:
    """单向链表类"""
    def __init__(self):
        self.head = None  # 头节点
        self.size = 0     # 链表长度
    
    def append(self, data):
        """在链表末尾添加节点"""
        new_node = Node(data)
        self.size += 1
        
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def prepend(self, data):
        """在链表开头添加节点"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert(self, index, data):
        """在指定位置插入节点"""
        if index < 0 or index > self.size:
            raise IndexError("索引超出范围")
        
        if index == 0:
            self.prepend(data)
            return
        
        if index == self.size:
            self.append(data)
            return
        
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete(self, data):
        """删除第一个匹配的节点"""
        if not self.head:
            return False
        
        # 如果头节点就是要删除的节点
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return True
        
        # 查找要删除的节点
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def delete_at(self, index):
        """删除指定位置的节点"""
        if index < 0 or index >= self.size:
            raise IndexError("索引超出范围")
        
        if index == 0:
            self.head = self.head.next
            self.size -= 1
            return
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        current.next = current.next.next
        self.size -= 1
    
    def find(self, data):
        """查找节点位置，返回第一个匹配的索引"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1
    
    def get(self, index):
        """获取指定位置的节点数据"""
        if index < 0 or index >= self.size:
            raise IndexError("索引超出范围")
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def display(self):
        """打印链表"""
        elements = []
        current = self.head
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements) + " -> None")
    
    def reverse(self):
        """反转链表"""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
    
    def __len__(self):
        return self.size
    
    def __iter__(self):
        """使链表可迭代"""
        current = self.head
        while current:
            yield current.data
            current = current.next
# 创建链表
ll = LinkedList()

# 添加元素
ll.append(1)
ll.append(2)
ll.append(3)
ll.prepend(0)
ll.display()  # 0 -> 1 -> 2 -> 3 -> None

# 插入元素
ll.insert(2, 1.5)
ll.display()  # 0 -> 1 -> 1.5 -> 2 -> 3 -> None

# 删除元素
ll.delete(1.5)
ll.display()  # 0 -> 1 -> 2 -> 3 -> None

# 查找元素
print(ll.find(2))   # 2
print(ll.find(10))  # -1

# 获取元素
print(ll.get(2))    # 2

# 遍历链表
for data in ll:
    print(data)     # 0 1 2 3

# 反转链表
ll.reverse()
ll.display()  # 3 -> 2 -> 1 -> 0 -> None

# 链表长度
print(len(ll))  # 4


