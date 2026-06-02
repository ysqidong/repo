from typing import Iterable, Any

class FindIndex:
    """
    给定一个可迭代对象，以及要查询的元素，返回索引，未找到返回-1
    """
    def __init__(self, iterable: Iterable[Any]):
        """
        :param iterable: 可迭代对象，查找其内部元素
        """
        self.iterable: list[Any] = list(iterable)

    def find(self, element: Any) -> int:
        """
        找到指定元素，返回索引，未找到返回-1

        :param element: 要找的元素
        :return: 索引
        """
        index: int
        element_in_iterable: Any
        for index, element_in_iterable in enumerate(self.iterable):
            if element_in_iterable == element:
                return index
                break

        return -1

number_list = [i for i in range(100_000_000)]

f = FindIndex(number_list)

print(f.find(1))
print(f.find(1))
print(f.find(1))
print(f.find(1))
print(f.find(1))

print(FindIndex(number_list).find(1))
