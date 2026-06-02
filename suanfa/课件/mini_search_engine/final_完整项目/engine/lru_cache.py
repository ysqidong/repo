"""
LRU 缓存模块 (lru_cache.py)
功能：基于单链表实现 LRU (Least Recently Used) 缓存
LRU 的意思是"最近最少使用"：当缓存满了的时候，把最久没被访问过的数据淘汰掉
"""


class Node:
    """
    链表节点类
    链表里的每一个小盒子就是一个节点，每个节点保存数据和下一个节点的地址
    """

    def __init__(self, data: tuple[str, list[str]]) -> None:
        # data 是这个节点保存的数据
        # 在 LRU 缓存中，我们存的是一个元组 (key, value)
        self.data = data
        # next 是指向下一个节点的指针，一开始没有下一个节点，所以是 None
        self.next = None


class LinkedList:
    """
    单向链表类
    链表有一个头节点 head，顺着 head 可以访问链表里的所有节点
    """

    def __init__(self) -> None:
        # head 是链表的第一个节点，一开始链表是空的，所以 head 为 None
        self.head = None
        # size 记录链表里有多少个节点
        self.size = 0

    def insert_at_head(self, data: tuple[str, list[str]]) -> None:
        """
        在链表头部插入一个新节点
        这是链表最常用、最快的插入方式，时间复杂度是 O(1)

        - 参数 data：要插入的节点数据
        """
        # 创建一个新节点
        new_node = Node(data)
        # 让新节点的 next 指向原来的头节点
        new_node.next = self.head
        # 让 head 指向新节点，新节点就变成了头节点
        self.head = new_node
        # 节点数量加 1
        self.size = self.size + 1

    def delete_node(self, target_data: tuple[str, list[str]]) -> None:
        """
        删除链表中 data 等于 target_data 的第一个节点

        - 参数 target_data：要删除的节点数据
        """
        # 如果链表是空的，直接返回
        if self.head is None:
            return

        # 如果要删除的是头节点
        if self.head.data == target_data:
            # 让 head 指向下一个节点，原来的头节点就被"丢掉"了
            self.head = self.head.next
            # 节点数量减 1
            self.size = self.size - 1
            return

        # 从头节点开始遍历链表
        current = self.head
        while current.next is not None:
            # 如果下一个节点就是要删除的节点
            if current.next.data == target_data:
                # 让当前节点的 next 跳过下一个节点，直接指向下下个节点
                current.next = current.next.next
                # 节点数量减 1
                self.size = self.size - 1
                return
            # 否则继续往后走
            current = current.next

    def delete_tail(self) -> None:
        """
        删除链表的尾节点（最后一个节点）
        """
        # 如果链表是空的，直接返回
        if self.head is None:
            return

        # 如果链表只有一个节点
        if self.head.next is None:
            # 把头节点设为 None，链表就空了
            self.head = None
            self.size = self.size - 1
            return

        # 找到倒数第二个节点
        current = self.head
        while current.next.next is not None:
            current = current.next

        # 让倒数第二个节点的 next 变成 None，最后一个节点就被"丢掉"了
        current.next = None
        self.size = self.size - 1

    def find(self, target_key: str) -> list[str] | None:
        """
        在链表中查找 key 等于 target_key 的节点

        - 参数 target_key：要查找的 key
        - 返回：对应的 value，如果找不到返回 None
        """
        # 从头节点开始遍历
        current = self.head
        while current is not None:
            # 我们的 data 是 (key, value) 的元组
            key, value = current.data
            # 如果 key 匹配，返回对应的 value
            if key == target_key:
                return value
            # 继续往后走
            current = current.next
        # 遍历完了都没找到，返回 None
        return None

    def move_to_head(self, target_key: str) -> None:
        """
        把 key 等于 target_key 的节点移动到链表头部
        这是 LRU 策略的核心：被访问过的数据要放到最前面

        - 参数 target_key：要移动的节点的 key
        """
        # 如果链表为空，直接返回
        if self.head is None:
            return

        # 如果头节点就是要移动的节点，直接返回（已经在头部了）
        if self.head.data[0] == target_key:
            return

        # 遍历找前一个节点，摘下目标节点，头插
        prev = self.head
        while prev.next is not None:
            if prev.next.data[0] == target_key:
                target_node = prev.next
                prev.next = target_node.next
                self.size = self.size - 1
                target_node.next = self.head
                self.head = target_node
                self.size = self.size + 1
                return
            prev = prev.next

    def to_list(self) -> list[tuple[str, list[str]]]:
        """
        把链表转换成一个 Python 列表，方便打印查看

        - 返回：包含链表中所有 data 的列表
        """
        # 准备一个空列表作为结果
        result: list[tuple[str, list[str]]] = []
        # 从头节点开始遍历
        current = self.head
        while current is not None:
            # 把当前节点的数据加到结果列表里
            result.append(current.data)
            # 继续往后走
            current = current.next
        return result


class LRUCache:
    """
    LRU 缓存类
    LRU = Least Recently Used，最近最少使用
    意思是：当缓存满了的时候，把最久没被访问过的数据淘汰掉
    我们把最近使用的放在链表头部，最久未使用的放在链表尾部
    """

    def __init__(self, capacity: int) -> None:
        # capacity 是缓存的最大容量（最多能存多少个 key-value 对）
        self.capacity = capacity
        # 用链表来保存缓存数据
        self.cache_list = LinkedList()

    def get(self, key: str) -> list[str] | None:
        """
        获取缓存中的数据
        如果 key 存在，把这个节点移到头部（表示最近使用了），返回 value
        如果 key 不存在，返回 None

        - 参数 key：要查找的 key
        - 返回：对应的 value 或 None
        """
        # 先在链表中查找
        value = self.cache_list.find(key)
        if value is not None:
            # 找到了！把它移到头部，表示最近使用过
            self.cache_list.move_to_head(key)
            return value
        # 没找到，返回 None
        return None

    def put(self, key: str, value: list[str]) -> None:
        """
        向缓存中放入数据
        如果 key 已存在，更新 value 并移到头部
        如果 key 不存在，在头部插入新节点；如果满了，删除尾部节点

        - 参数 key：数据的 key
        - 参数 value：数据的 value
        """
        # 先检查 key 是否已经存在
        existing = self.cache_list.find(key)
        if existing is not None:
            # 已存在，先删除旧节点，再插入更新后的节点到头部
            self.cache_list.delete_node((key, existing))
            self.cache_list.insert_at_head((key, value))
            return

        # 如果缓存还没满，直接在头部插入
        if self.cache_list.size < self.capacity:
            self.cache_list.insert_at_head((key, value))
        else:
            # 缓存满了，先删除尾部（最久未使用的），再在头部插入新的
            self.cache_list.delete_tail()
            self.cache_list.insert_at_head((key, value))
