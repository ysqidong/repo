from typing import Iterable, Any

class DeleteItem: 
    """
    管理列表的插入与删除操作
    """
    def __init__(self, iterable: Iterable[Any]):
        """
        初始化对象
        :param iterable: 可迭代对象，将其内部插入元素
        """
        self.iterable = list(iterable)

    def delete_by_index(self, index: int) -> list[Any]:
        """
        根据索引从列表中删除元素
        
        :param index: 要删除元素的索引位置
        :return: 删除元素后的列表
        """
        if 0 <= index < len(self.iterable):
            self.iterable.pop(index)
        else:
            print("索引超出范围")
        return self.iterable

    def delete_by_value(self, element: Any) -> list[Any]:
        """
        根据值从列表中删除元素（仅删除第一个匹配项）
        
        :param element: 要删除的具体元素
        :return: 删除元素后的列表
        """
        if element in self.iterable:
            self.iterable.remove(element)
        else:
            print(f"元素 {element} 不在列表中")
        return self.iterable
fruits=["apple", "banana", "cherry", "date", "fig", "grape"]
manager = DeleteItem(fruits)
print(manager.delete_by_index(2))  # 删除索引为2的元素