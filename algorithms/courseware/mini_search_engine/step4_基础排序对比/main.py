# 第四步：三种基础排序

# 比较的对象是tuple[str, int]
# 按字典序比较
# 首先比较index = 0的元素
# 比较结果相等则比较index = 1

# 字典序内，字符串先比较第一个字母

import time
import random


def bubble_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    冒泡排序

    - 参数 arr：一个列表
    - 返回：排好序的列表
    """

    # 先复制一份原列表，不要修改原来的数据
    # 使用全量切片的方式
    arr_new = arr[:]

    # 获取列表的长度
    n = len(arr_new)

    # 外层循环控制要进行多少轮
    # 有 n 个数字，最多需要 n-1 轮
    for i in range(n - 1):
        # 内层循环负责每一轮的比较和交换
        # 每一轮结束后，最右边的 i 个数字已经排好了，所以范围是 0 到 n-1-i
        for j in range(n - 1 - i):
            # 如果左边的数字比右边大，就交换它们
            if arr_new[j] > arr_new[j + 1]:
                # 交换两个数字的位置
                temp = arr_new[j]
                arr_new[j] = arr_new[j + 1]
                arr_new[j + 1] = temp

    return arr_new


def selection_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    选择排序

    - 参数 arr：一个列表
    - 返回：排好序的列表
    """
    # 复制原列表
    arr_new = arr[:]
    n = len(arr_new)

    # 外层循环：i 表示当前要放最小数字的位置
    for i in range(n - 1):
        # 假设当前位置 i 的数字就是最小的
        min_index = i

        # 内层循环：从 i 后面的数字里找真正的最小值
        for j in range(i + 1, n):
            if arr_new[j] < arr_new[min_index]:
                # 找到更小的数字，记录它的位置
                min_index = j

        # 一轮找完后，把最小数字和位置 i 的数字交换
        if min_index != i:
            temp = arr_new[i]
            arr_new[i] = arr_new[min_index]
            arr_new[min_index] = temp

    return arr_new


def insertion_sort(arr: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """
    插入排序

    - 参数 arr：一个列表
    - 返回：排好序的列表
    """
    # 复制原列表
    arr_new = arr[:]
    n = len(arr_new)

    # 从第 2 个数字开始（索引是 1），逐个插入到前面的有序序列中
    for i in range(1, n):
        # 取出当前要插入的数字
        current = arr_new[i]
        # j 表示前面已排序部分的最后一个位置
        j = i - 1

        # 从后往前找，如果前面的数字比 current 大，就往后挪一位
        while j >= 0 and arr_new[j] > current:
            arr_new[j + 1] = arr_new[j]
            j = j - 1

        # 找到合适的位置，把 current 放进去
        arr_new[j + 1] = current

    return arr_new


# =================== 主程序开始 ===================
if __name__ == "__main__":
    print("===== 第四步：三种基础排序对比 =====")
    print()

    # 准备一组搜索结果的模拟数据
    # 每个元素是一个元组：(文档名, 得分)
    search_result = [
        ("docH.txt", 41),
        ("docG.txt", 89),
        ("docF.txt", 23),
        ("docE.txt", 56),
        ("docD.txt", 5),
        ("docC.txt", 78),
        ("docB.txt", 12),
        ("docA.txt", 35),
    ]

    print("原始数据：", search_result)
    print()

    # ===== 测试冒泡排序 =====
    print("--- 冒泡排序 ---")
    start = time.time()  # 记录开始时间
    result1 = bubble_sort(search_result)
    end = time.time()  # 记录结束时间
    print("排序后：", result1)
    print("耗时：", round(end - start, 6), "秒")
    print()

    # ===== 测试选择排序 =====
    print("--- 选择排序 ---")
    start = time.time()
    result2 = selection_sort(search_result)
    end = time.time()
    print("排序后：", result2)
    print("耗时：", round(end - start, 6), "秒")
    print()

    # ===== 测试插入排序 =====
    print("--- 插入排序 ---")
    start = time.time()
    result3 = insertion_sort(search_result)
    end = time.time()
    print("排序后：", result3)
    print("耗时：", round(end - start, 6), "秒")
    print()

    # ===== 大数据对比 =====
    print("--- 大数据对比（1000 个随机数）---")
    # 生成 1000 个 0 到 999 之间的随机整数
    big_data: list[int] = []
    for _ in range(10000):
        big_data.append(random.randint(0, 999))

    # 冒泡排序测速
    start = time.time()
    bubble_sort(big_data)
    end = time.time()
    print("冒泡排序 1000 个数耗时：", round(end - start, 4), "秒")

    # 选择排序测速
    start = time.time()
    selection_sort(big_data)
    end = time.time()
    print("选择排序 1000 个数耗时：", round(end - start, 4), "秒")

    # 插入排序测速
    start = time.time()
    insertion_sort(big_data)
    end = time.time()
    print("插入排序 1000 个数耗时：", round(end - start, 4), "秒")
