"""
data_structure_7：二叉树层序遍历（BFS）
学号 24375352  王子昂

给定二叉树：
        10
       /  \
      5    15
     / \     \
    3   7    20

实现层序遍历（广度优先搜索），按层输出节点值。
"""

from collections import deque
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right


def build_tree(values: list) -> Optional[TreeNode]:
    """从 LeetCode 风格列表构建二叉树（None 表示空节点）"""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """
    层序遍历（BFS）
    返回按层分组的节点值列表
    """
    if not root:
        return []

    result: list[list[int]] = []
    q: deque[TreeNode] = deque([root])

    while q:
        level_size = len(q)
        level: list[int] = []
        for _ in range(level_size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)

    return result


def print_tree_structure(root: Optional[TreeNode]) -> None:
    """按层打印树结构"""
    if not root:
        print("空树")
        return
    q: deque[tuple[Optional[TreeNode], int]] = deque([(root, 0)])
    levels: dict[int, list] = {}
    while q:
        node, depth = q.popleft()
        levels.setdefault(depth, []).append(node.val if node else None)
        if node:
            q.append((node.left, depth + 1))
            q.append((node.right, depth + 1))

    print("二叉树层序遍历结构：")
    for depth in sorted(levels):
        print(f"  第{depth}层: {levels[depth]}")


# ==================== 测试 ====================
if __name__ == "__main__":
    values = [10, 5, 15, 3, 7, None, 20]
    root = build_tree(values)

    print("=" * 40)
    print_tree_structure(root)
    print("=" * 40)

    levels = level_order(root)
    print(f"\n层序遍历结果: {levels}")
    for i, lv in enumerate(levels):
        print(f"  第{i}层: {lv}")
