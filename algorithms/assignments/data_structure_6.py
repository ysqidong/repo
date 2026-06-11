"""
data_structure_6：链表进阶 — 反转 & 环检测
学号 24375352  王子昂

两个经典算法：
1. 单链表反转（迭代法，O(n) / O(1)）
2. 环检测（快慢指针 / Floyd 判圈）
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self) -> None:
        self.head: ListNode | None = None

    # ==================== 核心 ====================

    def reverse(self) -> None:
        """
        反转链表（原地）
          prev ← cur → next  →  prev ← cur → next
        """
        prev: ListNode | None = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def has_cycle(self) -> bool:
        """
        Floyd 判圈：快慢指针
        快走两步、慢走一步 → 相遇 = 有环
        """
        if not self.head or not self.head.next:
            return False
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    # ==================== 辅助 ====================

    def append(self, val) -> None:
        new = ListNode(val)
        if not self.head:
            self.head = new
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new

    def print_list(self) -> None:
        vals = []
        cur = self.head
        while cur:
            vals.append(str(cur.val))
            cur = cur.next
        print(" -> ".join(vals))


# ==================== 测试 ====================
if __name__ == "__main__":
    # 反转
    print("=== 链表反转 ===")
    ll = LinkedList()
    for v in ['a', 'b', 'c', 'd']:
        ll.append(v)
    print("原链表:", end=" ")
    ll.print_list()
    ll.reverse()
    print("反转后:", end=" ")
    ll.print_list()

    # 环检测
    print("\n=== 环检测 ===")
    l1 = LinkedList()
    for v in [1, 2, 3, 4]:
        l1.append(v)
    print(f"无环链表 → {l1.has_cycle()}")

    l2 = LinkedList()
    for v in [1, 2, 3]:
        l2.append(v)
    cur = l2.head
    while cur.next:
        cur = cur.next
    cur.next = l2.head     # 成环
    print(f"有环链表 → {l2.has_cycle()}")
