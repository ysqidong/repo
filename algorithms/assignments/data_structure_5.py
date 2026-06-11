"""
data_structure_5：单链表实现
学号 24375352  王子昂

实现 LinkedList 类：
- Node 节点类
- append / prepend / insert
- read / delete / delete_by_value
- length / find / get_all_data
"""

from typing import Any


class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next: Node | None = None

    def __repr__(self) -> str:
        return f"Node({self.data!r})"


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None

    # ---------- 增 ----------

    def append(self, data: Any) -> None:
        new = Node(data)
        if not self.head:
            self.head = new
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new

    def prepend(self, data: Any) -> None:
        new = Node(data)
        new.next = self.head
        self.head = new

    def insert(self, index: int, data: Any) -> None:
        if index == 0:
            self.prepend(data)
            return
        new = Node(data)
        cur = self.head
        for _ in range(index - 1):
            if cur is None:
                raise IndexError(f"索引 {index} 越界")
            cur = cur.next
        if cur is None:
            raise IndexError(f"索引 {index} 越界")
        new.next = cur.next
        cur.next = new

    # ---------- 查 ----------

    def read(self, index: int) -> Any | None:
        cur = self.head
        for _ in range(index):
            if cur is None:
                return None
            cur = cur.next
        return cur.data if cur else None

    def find(self, value: Any) -> int:
        cur = self.head
        idx = 0
        while cur:
            if cur.data == value:
                return idx
            cur = cur.next
            idx += 1
        return -1

    def length(self) -> int:
        count = 0
        cur = self.head
        while cur:
            count += 1
            cur = cur.next
        return count

    def get_all_data(self) -> list[Any]:
        result: list[Any] = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    # ---------- 删 ----------

    def delete(self, index: int) -> bool:
        if not self.head:
            return False
        if index == 0:
            self.head = self.head.next
            return True
        cur = self.head
        for _ in range(index - 1):
            if cur.next is None:
                return False
            cur = cur.next
        if cur.next is None:
            return False
        cur.next = cur.next.next
        return True

    def delete_by_value(self, value: Any) -> bool:
        if not self.head:
            return False
        if self.head.data == value:
            self.head = self.head.next
            return True
        cur = self.head
        while cur.next:
            if cur.next.data == value:
                cur.next = cur.next.next
                return True
            cur = cur.next
        return False

    # ---------- 输出 ----------

    def __str__(self) -> str:
        return " -> ".join(str(d) for d in self.get_all_data())


# ==================== 测试 ====================
if __name__ == "__main__":
    ll = LinkedList()
    ll.append("hello")
    ll.append("world")
    ll.append(42)
    ll.prepend("first")

    print("链表:", ll)
    print("长度:", ll.length())
    print("索引 2:", ll.read(2))
    print("查找 42:", ll.find(42))

    ll.insert(1, "inserted")
    print("索引1插入后:", ll)

    ll.delete_by_value(42)
    print("删除42后:", ll)

    ll.delete(0)
    print("删除索引0后:", ll)
    print("所有数据:", ll.get_all_data())
