class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    # 1. 链表反转
    def reverse(self):
        """反转链表，返回新的头节点"""
        prev = None
        curr = self.head
        while curr:
            next_temp = curr.next  # 暂存下一个节点
            curr.next = prev       # 当前节点指向前一个
            prev = curr            # 前移 prev
            curr = next_temp       # 前移 curr
        self.head = prev           # 更新头节点

    # 2. 检测环
    def has_cycle(self):
        """检测链表是否有环，使用快慢指针"""
        if not self.head:
            return False
        slow = self.head
        fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:   # 快慢指针相遇，有环
                return True
        return False

    # 辅助方法：从列表构建链表（无环）
    def from_list(self, arr):
        dummy = ListNode()
        curr = dummy
        for val in arr:
            curr.next = ListNode(val)
            curr = curr.next
        self.head = dummy.next

    # 辅助方法：创建环（用于测试，将尾节点指向第 index 个节点）
    def create_cycle(self, index):
        if not self.head or index < 0:
            return
        # 找到尾节点
        tail = self.head
        while tail.next:
            tail = tail.next
        # 找到第 index 个节点
        target = self.head
        for _ in range(index):
            if not target:
                return
            target = target.next
        if target:
            tail.next = target

    # 辅助方法：打印链表（需无环，否则死循环）
    def display(self):
        vals = []
        curr = self.head
        while curr:
            vals.append(str(curr.val))
            curr = curr.next
        print(" -> ".join(vals) if vals else "空链表")


# 测试演示
if __name__ == "__main__":
    # 测试反转
    ll = LinkedList()
    ll.from_list(['a', 'b', 'c'])
    print("原始链表:")
    ll.display()          # a -> b -> c
    ll.reverse()
    print("反转后:")
    ll.display()          # c -> b -> a

    # 测试环检测（无环）
    print("\n无环链表是否有环?", ll.has_cycle())  # False

    # 构造有环链表
    ll_cycle = LinkedList()
    ll_cycle.from_list([1, 2, 3, 4, 5])
    ll_cycle.create_cycle(2)   # 尾节点指向 3（索引2）
    print("有环链表是否有环?", ll_cycle.has_cycle())  # True