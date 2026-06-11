"""
历史记录模块 (history.py)
功能：用 Python 的 list 模拟栈和队列，记录用户的搜索历史
栈用来获取"上一次"搜索，队列用来获取"最近"搜索
"""


class Stack:
    """
    栈类：后进先出 (LIFO - Last In First Out)
    想象一叠盘子，最后放上去的盘子最先被拿走
    这里我们用 Python 列表来模拟栈
    """

    def __init__(self) -> None:
        # 用一个空列表来存储栈中的元素
        # 列表的末尾就是栈顶
        self.items: list[str] = []

    def push(self, item: str) -> None:
        """
        入栈操作：把一个元素放到栈顶

        - 参数 item：要放入栈中的元素
        """
        # 用 append 把元素加到列表末尾，这就是栈顶
        self.items.append(item)

    def pop(self) -> str | None:
        """
        出栈操作：移除并返回栈顶元素

        - 返回：栈顶元素，如果栈为空则返回 None
        """
        # 先检查栈是否为空
        if len(self.items) == 0:
            return None
        # 用 pop() 移除并返回列表的最后一个元素
        return self.items.pop()

    def top(self) -> str | None:
        """
        查看栈顶元素：不移除，只返回

        - 返回：栈顶元素，如果栈为空则返回 None
        """
        # 先检查栈是否为空
        if len(self.items) == 0:
            return None
        # 返回列表的最后一个元素（索引 -1）
        return self.items[-1]

    def size(self) -> int:
        """
        获取栈中元素的个数

        - 返回：元素数量（整数）
        """
        # 返回列表的长度
        return len(self.items)


class Queue:
    """
    队列类：先进先出 (FIFO - First In First Out)
    想象排队买票，先排队的人先买到票
    这里我们用 Python 列表来模拟队列
    """

    def __init__(self) -> None:
        # 用一个空列表来存储队列中的元素
        self.items: list[str] = []

    def enqueue(self, item: str) -> None:
        """
        入队操作：把一个元素放到队列末尾

        - 参数 item：要放入队列的元素
        """
        # 用 append 把元素加到列表末尾，这就是队尾
        self.items.append(item)

    def dequeue(self) -> str | None:
        """
        出队操作：移除并返回队列最前面的元素

        - 返回：队首元素，如果队列为空则返回 None
        """
        # 先检查队列是否为空
        if len(self.items) == 0:
            return None
        # 注意：这里用 list.pop(0) 是为了教学简单，真实工程中大批量数据建议使用 collections.deque
        # 用 pop(0) 移除并返回列表的第一个元素，这就是队首
        return self.items.pop(0)

    def front(self) -> str | None:
        """
        查看队首元素：不移除，只返回

        - 返回：队首元素，如果队列为空则返回 None
        """
        # 先检查队列是否为空
        if len(self.items) == 0:
            return None
        # 返回列表的第一个元素（索引 0）
        return self.items[0]

    def size(self) -> int:
        """
        获取队列中元素的个数

        - 返回：元素数量（整数）
        """
        # 返回列表的长度
        return len(self.items)

    def get_all(self) -> list[str]:
        """
        获取队列中所有元素的副本

        - 返回：一个包含所有元素的列表（不会修改原队列）
        """
        # 用切片 [:] 复制一份列表返回
        return self.items[:]
