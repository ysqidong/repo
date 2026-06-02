"""
有序词表模块 (sorted_terms.py)
功能：维护有序数组，并提供二分查找功能
当我们需要快速判断一个词语是否存在于索引中时，有序数组 + 二分查找非常有用
"""


def binary_search(arr: list[str], target: str) -> int:
    """
    二分查找函数（非递归实现）
    原理：每次都把搜索范围缩小一半，效率非常高

    - 参数 arr：已经排好序的列表
    - 参数 target：我们要找的目标值
    - 返回：如果找到了，返回目标值的索引；如果没找到，返回 -1
    """
    # 左边界从数组的第一个位置（索引 0）开始
    left = 0
    # 右边界从数组的最后一个位置开始
    right = len(arr) - 1

    # 当左边界不超过右边界时，继续查找
    while left <= right:
        # 计算中间位置
        # 用 left + (right - left) // 2 而不是 (left + right) // 2
        # 是为了防止数字太大时溢出（虽然在 Python 中不太需要担心）
        mid = left + (right - left) // 2

        # 比较中间值和目标值
        if arr[mid] == target:
            # 找到了！返回中间位置的索引
            return mid
        elif arr[mid] < target:
            # 中间值比目标小，说明目标在右半边
            # 把左边界移到中间位置的右边
            left = mid + 1
        else:
            # 中间值比目标大，说明目标在左半边
            # 把右边界移到中间位置的左边
            right = mid - 1

    # 如果循环结束了还没找到，说明数组里没有目标值
    return -1


def get_sorted_terms(index: dict[str, list[str]]) -> list[str]:
    """
    从索引中提取所有词并排序

    - 参数 index：倒排索引字典（格式是 {word: [docs]}）
    - 返回：按字母/拼音顺序排序后的词列表
    """
    # 准备一个空列表，用来装所有词语
    terms: list[str] = []

    # 遍历字典中的每一个 key（也就是每一个词语）
    for word in index:
        # 把这个词语加到列表里
        terms.append(word)

    # 用 Python 内置的 sorted() 函数对列表进行排序
    # sorted() 会返回一个新的有序列表，不会修改原来的列表
    return sorted(terms)
