import random

# ========== 1. 优化快速排序（随机选择轴）==========
def quick_sort_optimized(arr, left=0, right=None):
    if right is None:
        right = len(arr) - 1
    
    if left >= right:
        return arr
    
    # 随机选择轴并交换到末尾
    random_index = random.randint(left, right)
    arr[random_index], arr[right] = arr[right], arr[random_index]
    
    # 分区
    pivot_index = partition(arr, left, right)
    
    # 递归排序左右两部分
    quick_sort_optimized(arr, left, pivot_index - 1)
    quick_sort_optimized(arr, pivot_index + 1, right)
    
    return arr

def partition(arr, left, right):
    """分区函数：将小于轴的放左边，大于轴的放右边"""
    pivot = arr[right]
    i = left  # i 指向小于区域的边界
    
    for j in range(left, right):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    
    # 将轴放到正确位置
    arr[i], arr[right] = arr[right], arr[i]
    return i


# ========== 2. 三路快速排序（处理大量重复元素）==========
def quick_sort_3way(arr, left=0, right=None):
    """
    三路快排：将数组分为 [小于轴] [等于轴] [大于轴] 三部分
    特别适合有大量重复元素的数组
    """
    if right is None:
        right = len(arr) - 1
    
    if left >= right:
        return arr
    
    # 随机选择轴
    random_index = random.randint(left, right)
    arr[random_index], arr[left] = arr[left], arr[random_index]
    
    pivot = arr[left]
    
    # 三路分区指针
    lt = left      # arr[left+1...lt] < pivot
    i = left + 1   # arr[lt+1...i-1] == pivot
    gt = right     # arr[gt...right] > pivot
    
    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:  # arr[i] == pivot
            i += 1
    
    # 递归处理小于和大于部分（等于部分已经在中间，不用处理）
    quick_sort_3way(arr, left, lt - 1)
    quick_sort_3way(arr, gt + 1, right)
    
    return arr


# ========== 测试代码 ==========
if __name__ == "__main__":
    # 测试1：普通数组
    print("=" * 50)
    print("测试1：普通数组")
    arr1 = [3, 6, 8, 10, 1, 2, 1]
    print(f"原数组: {arr1}")
    print(f"优化快排: {quick_sort_optimized(arr1.copy())}")
    
    # 测试2：大量重复元素（三路快排的优势场景）
    print("\n" + "=" * 50)
    print("测试2：大量重复元素数组")
    arr2 = [2, 2, 1, 1, 3, 3, 2, 1, 3, 2, 1, 1, 2, 3, 2]
    print(f"原数组: {arr2}")
    print(f"三路快排: {quick_sort_3way(arr2.copy())}")
    
    # 测试3：已排序数组（最坏情况测试）
    print("\n" + "=" * 50)
    print("测试3：已排序数组（避免最坏情况）")
    arr3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"原数组: {arr3}")
    print(f"优化快排: {quick_sort_optimized(arr3.copy())}")
    
    # 测试4：倒序数组
    print("\n" + "=" * 50)
    print("测试4：倒序数组")
    arr4 = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    print(f"原数组: {arr4}")
    print(f"优化快排: {quick_sort_optimized(arr4.copy())}")
    
    # 测试5：性能对比（大量重复元素）
    print("\n" + "=" * 50)
    print("测试5：大量重复元素性能对比")
    arr5 = [random.choice([1, 2, 3]) for _ in range(20)]
    print(f"原数组: {arr5}")
    print(f"优化快排结果: {quick_sort_optimized(arr5.copy())}")
    print(f"三路快排结果: {quick_sort_3way(arr5.copy())}")