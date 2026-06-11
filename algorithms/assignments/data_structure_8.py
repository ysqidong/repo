"""
data_structure_8：BST 删除策略 — 中序前驱 vs 中序后继
学号 24375352  王子昂

题1：构建 BST，插入 [50, 30, 70, 20, 40, 60, 80]
题2：删除根结点 50，分别用中序前驱、中序后继两种策略
题3：讨论实际项目用哪种策略及原因
"""

from __future__ import annotations
from typing import Optional


class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BST:
    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    # ==================== 基础操作 ====================

    def insert(self, val: int) -> None:
        if self.root is None:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node: TreeNode, val: int) -> None:
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert(node.left, val)
        elif val > node.val:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert(node.right, val)

    def inorder(self) -> list[int]:
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: Optional[TreeNode], result: list[int]) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    # ==================== 辅助查找 ====================

    @staticmethod
    def find_min(node: TreeNode) -> TreeNode:
        """找子树最小值（最左）"""
        while node.left:
            node = node.left
        return node

    @staticmethod
    def find_max(node: TreeNode) -> TreeNode:
        """找子树最大值（最右）"""
        while node.right:
            node = node.right
        return node

    # ==================== 删除策略 ====================

    def delete_predecessor(self, val: int) -> None:
        """删除 — 中序前驱策略（左子树最大值替换）"""
        self.root = self._del_pre(self.root, val)

    def _del_pre(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if node is None:
            return None
        if val < node.val:
            node.left = self._del_pre(node.left, val)
        elif val > node.val:
            node.right = self._del_pre(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # 两个孩子：中序前驱
            pred = self.find_max(node.left)
            node.val = pred.val
            node.left = self._del_pre(node.left, pred.val)
        return node

    def delete_successor(self, val: int) -> None:
        """删除 — 中序后继策略（右子树最小值替换）"""
        self.root = self._del_suc(self.root, val)

    def _del_suc(self, node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        if node is None:
            return None
        if val < node.val:
            node.left = self._del_suc(node.left, val)
        elif val > node.val:
            node.right = self._del_suc(node.right, val)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # 两个孩子：中序后继
            succ = self.find_min(node.right)
            node.val = succ.val
            node.right = self._del_suc(node.right, succ.val)
        return node

    # ==================== 可视化（文本版） ====================

    def print_tree(self) -> None:
        """横向打印 BST"""
        self._print(self.root, 0, "ROOT")

    def _print(self, node: Optional[TreeNode], depth: int, tag: str) -> None:
        if node is None:
            return
        self._print(node.right, depth + 1, "R")
        print("    " * depth + f"[{tag}] {node.val}")
        self._print(node.left, depth + 1, "L")


# ==================== 测试 ====================
if __name__ == "__main__":
    # 题1：构建 BST
    bst = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(v)

    print("题1：构建 BST")
    print("  中序遍历:", bst.inorder())
    bst.print_tree()

    # 题2-策略一：中序前驱
    bst_pre = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst_pre.insert(v)
    bst_pre.delete_predecessor(50)

    print("\n题2-策略一：中序前驱删除 50")
    print("  新根:", bst_pre.root.val if bst_pre.root else None)
    print("  中序遍历:", bst_pre.inorder())
    bst_pre.print_tree()

    # 题2-策略二：中序后继
    bst_suc = BST()
    for v in [50, 30, 70, 20, 40, 60, 80]:
        bst_suc.insert(v)
    bst_suc.delete_successor(50)

    print("\n题2-策略二：中序后继删除 50")
    print("  新根:", bst_suc.root.val if bst_suc.root else None)
    print("  中序遍历:", bst_suc.inorder())
    bst_suc.print_tree()

    # 题3：讨论
    print("""
============================================================
题3：实际项目用哪一种？

结论：中序后继（右子树最小值）更常见。

原因：
1. 多数标准库默认后继：C++ std::set/map、Java TreeMap、CLRS 伪代码
2. 与 delete_min 操作一致，代码可复用
3. 随机数据下不容易破坏平衡
4. 自平衡树（AVL/红黑树）中两者效果相同，选后继是工程习惯
============================================================
""")
