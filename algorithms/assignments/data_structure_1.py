"""
data_structure_1：手动实现删除元素
学号 24375352  王子昂

不借助 list.pop(index)，通过元素前移 + pop() 尾删实现按下标删除。
"""

from typing import Iterable, Any


class DeleteItem:
    """手动实现列表删除操作"""

    def __init__(self, iterable: Iterable[Any]):
        self.iterable: list[Any] = list(iterable)

    def delete_by_index(self, index: int) -> list[Any]:
        """
        手动按下标删除（不调用 pop(index)）
        思路：从 index 开始，每个元素向前移动一格，最后 pop 掉末尾
        """
        length = len(self.iterable)
        if index < 0 or index >= length:
            print(f"索引 {index} 超出范围")
            return self.iterable

        for i in range(index, length - 1):
            self.iterable[i] = self.iterable[i + 1]

        self.iterable.pop()  # 删除末尾多余元素
        return self.iterable

    def delete_by_value(self, element: Any) -> list[Any]:
        """按值删除第一个匹配项"""
        for i, item in enumerate(self.iterable):
            if item == element:
                return self.delete_by_index(i)
        print(f"元素 {element} 不在列表中")
        return self.iterable


# ==================== 测试 ====================
if __name__ == "__main__":
    fruits = ["apple", "banana", "orange", "cherry", "mango"]
    manager = DeleteItem(fruits)

    print("原始列表:", fruits)
    print("删除索引 2:", manager.delete_by_index(2))
    print("删除值 'mango':", manager.delete_by_value("mango"))
    print("删除值 'not_exist':", manager.delete_by_value("not_exist"))
