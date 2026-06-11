"""
排序模块 (ranker.py)
功能：提供四种排序算法，并支持搜索结果排序
这个模块让我们可以对比不同排序算法的效率，也能给搜索结果按相关度排序
"""

import random  # 导入 random 模块，用来生成随机测试数据
import time    # 导入 time 模块，用来测量算法运行时间


def bubble_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    冒泡排序函数
    原理：重复走访要排序的列表，一次比较两个相邻元素，如果顺序不对就交换
    就像气泡一样，大的数会慢慢"浮"到右边

    - 参数 arr：要排序的列表
    - 返回：排序后的新列表
    """
    # 先复制一份原列表，避免修改原始数据
    nums = arr[:]
    # n 是列表的长度
    n = len(nums)

    # 外层循环：需要进行 n-1 轮比较
    for i in range(n - 1):
        # 内层循环：每轮把当前最大的数"冒泡"到右边
        # 因为右边已经排好序的部分不需要再比较，所以范围是 n-1-i
        for j in range(n - 1 - i):
            # 如果左边的数比右边大，就交换它们
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]

    # 返回排好序的列表
    return nums


def selection_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    选择排序函数
    原理：每一轮从剩余元素中选出最小的，放到已排序序列的末尾

    - 参数 arr：要排序的列表
    - 返回：排序后的新列表
    """
    # 先复制一份原列表
    nums = arr[:]
    # n 是列表的长度
    n = len(nums)

    # 外层循环：依次确定第 0, 1, 2, ... 个位置的元素
    for i in range(n - 1):
        # 假设当前位置 i 就是最小值的位置
        min_idx = i

        # 从 i 的后面开始找，看看有没有更小的
        for j in range(i + 1, n):
            if nums[j] < nums[min_idx]:
                # 找到更小的，更新最小值的索引
                min_idx = j

        # 如果最小值不是当前位置，就交换
        if min_idx != i:
            nums[i], nums[min_idx] = nums[min_idx], nums[i]

    # 返回排好序的列表
    return nums


def insertion_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    插入排序函数
    原理：把列表分成"已排序"和"未排序"两部分，逐个把未排序的元素插入到已排序部分的正确位置
    就像打牌时整理手牌一样

    - 参数 arr：要排序的列表
    - 返回：排序后的新列表
    """
    # 先复制一份原列表
    nums = arr[:]
    # n 是列表的长度
    n = len(nums)

    # 从第 2 个元素开始（索引为 1），因为第 1 个元素默认已排序
    for i in range(1, n):
        # current 是当前要插入的元素
        current = nums[i]
        # j 是当前元素的前一个位置
        j = i - 1

        # 把比 current 大的元素都往后挪一位
        while j >= 0 and nums[j] > current:
            nums[j + 1] = nums[j]
            j = j - 1

        # 在腾出的空位上放入 current
        nums[j + 1] = current

    # 返回排好序的列表
    return nums


# 这是教学版的快速排序，会创建新列表，大数据量时内存开销较大
def quick_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    快速排序函数（递归实现）
    原理：选一个"基准值"，把小于基准的放左边，大于基准的放右边，然后对两边递归排序

    - 参数 arr：要排序的列表
    - 返回：排序后的新列表
    """
    # 如果列表长度小于等于 1，不需要排序，直接返回副本
    if len(arr) <= 1:
        return arr[:]

    # 选第一个元素作为基准值（pivot）
    pivot = arr[0]

    # smaller 用来装所有小于 pivot 的元素
    smaller: list[tuple[str, int]] = []
    # larger 用来装所有大于等于 pivot 的元素
    larger: list[tuple[str, int]] = []

    # 从第 2 个元素开始遍历
    for i in range(1, len(arr)):
        if arr[i] < pivot:
            smaller.append(arr[i])
        else:
            larger.append(arr[i])

    # 递归排序左右两边，再把结果拼接起来：左 + pivot + 右
    return quick_sort(smaller) + [pivot] + quick_sort(larger)


def rank_results(index: dict[str, list[str]], words: list[str]) -> list[tuple[str, int]]:
    """
    多关键词搜索并排序
    原理：统计每个文档匹配了多少个搜索词，匹配越多的文档排名越靠前

    - 参数 index：倒排索引（字典）
    - 参数 words：搜索词列表
    - 返回：按相关度降序排列的 (文档名, 得分) 列表
    """
    # 准备一个空字典，用来统计每个文档的得分
    # key 是文档名，value 是匹配到的搜索词数量
    scores: dict[str, int] = {}

    # 遍历每一个搜索词
    for word in words:
        # 如果这个词在索引里存在
        if word in index:
            # 遍历包含这个词的每一个文档
            for doc in index[word]:
                # 给这个文档的得分加 1
                # scores.get(doc, 0) 表示如果文档还没有得分，默认是 0
                scores[doc] = scores.get(doc, 0) + 1

    # 转换为 (score, doc) 的元组列表，方便用快速排序排序
    # 排序规则：按匹配词数量（score）降序排列；如果 score 相同，文档名字典序小的排在前面
    items: list[tuple[int, str]] = []
    for doc, score in scores.items():
        items.append((score, doc))

    # 用快速排序对列表进行排序
    sorted_items = quick_sort(items)

    # 反转列表，得到降序结果（得分高的在前面）
    sorted_items = sorted_items[::-1]

    # 转换回 (doc, score) 格式
    result: list[tuple[str, int]] = []
    for score, doc in sorted_items:
        result.append((doc, score))

    # 返回排序后的搜索结果
    return result
