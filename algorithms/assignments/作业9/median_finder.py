"""

================================================================================
  MedianFinder — 双堆求中位数
  =============================
  用一个大顶堆（左半）和一个小顶堆（右半）动态维护数据流的中位数。

  不变量:
    len(maxHeap) == len(minHeap)  或  len(maxHeap) == len(minHeap) + 1

  时间复杂度:
    addNum      O(log n)
    findMedian  O(1)
================================================================================
"""

import heapq


class MedianFinder:
    """
    双堆数据结构，动态返回数据流的中位数。

    示例
    ----
    >>> mf = MedianFinder()
    >>> mf.addNum(10); mf.findMedian()
    10.0
    >>> mf.addNum(20); mf.findMedian()
    15.0
    >>> mf.addNum(5);  mf.findMedian()
    10.0
    >>> mf.addNum(25); mf.findMedian()
    15.0
    >>> mf.addNum(30); mf.findMedian()
    20.0
    """

    def __init__(self):
        # 大顶堆（左半）：存较小的那一半数。
        # Python heapq 是小顶堆，通过取负值模拟大顶堆。
        self.maxHeap: list[int] = []

        # 小顶堆（右半）：存较大的那一半数。
        self.minHeap: list[int] = []

    # ------------------------------------------------------------------
    # 核心操作
    # ------------------------------------------------------------------

    def addNum(self, num: int) -> None:
        """
        添加一个整数，维护双堆不变量。

        步骤:
          1. num 先入 maxHeap（左半）
          2. maxHeap 最大值弹出并入 minHeap（保证左 ≤ 右）
          3. 若 minHeap 比 maxHeap 大，minHeap 最小值弹回 maxHeap（平衡大小）
        """
        # Step 1 & 2：先放左，再最大值转到右
        heapq.heappush(self.maxHeap, -num)
        heapq.heappush(self.minHeap, -heapq.heappop(self.maxHeap))

        # Step 3：平衡（保证 maxHeap >= minHeap）
        if len(self.minHeap) > len(self.maxHeap):
            heapq.heappush(self.maxHeap, -heapq.heappop(self.minHeap))

    def findMedian(self) -> float:
        """
        返回当前所有已添加数字的中位数。

        O(1) — 直接读堆顶。
        """
        if len(self.maxHeap) > len(self.minHeap):
            return float(-self.maxHeap[0])
        return (-self.maxHeap[0] + self.minHeap[0]) / 2.0

    # ------------------------------------------------------------------
    # 辅助方法（调试用）
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self.maxHeap) + len(self.minHeap)

    def snapshot(self) -> str:
        """返回当前双堆状态的字符串表示。"""
        left = sorted([-x for x in self.maxHeap], reverse=True)
        right = sorted(self.minHeap)
        return f"左(maxHeap)={left}  右(minHeap)={right}"


# ================================================================================
# 测试
# ================================================================================
if __name__ == "__main__":
    import sys

    mf = MedianFinder()

    # ---- test 1: 课件示例序列 ----
    print("=" * 60)
    print("Test 1: 课件示例")
    print("=" * 60)
    expected = [10.0, 15.0, 10.0, 15.0, 20.0]
    for i, num in enumerate([10, 20, 5, 25, 30]):
        mf.addNum(num)
        got = mf.findMedian()
        status = "OK" if got == expected[i] else "FAIL"
        print(f"  addNum({num:>2})  ->  {mf.snapshot():<45s}  中位数={got}  {status}")
    print()

    # ---- test 2: 随机大数据量压力 ----
    print("=" * 60)
    print("Test 2: 随机 10000 个数，与排序结果比对")
    print("=" * 60)
    import random

    mf2 = MedianFinder()
    data = [random.randint(-10000, 10000) for _ in range(10000)]
    ok = 0
    for i, x in enumerate(data, 1):
        mf2.addNum(x)
        if i % 2000 == 0:
            sorted_data = sorted(data[:i])
            n = len(sorted_data)
            true_median = (
                sorted_data[n // 2]
                if n % 2 == 1
                else (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2.0
            )
            got = mf2.findMedian()
            if got == true_median:
                ok += 1
            else:
                print(f"  FAIL i={i}: got={got}, expected={true_median}")
    print(f"  抽查 {ok}/{5} 次全部通过")
    print()

    # ---- test 3: 奇数个、偶数个中位数 ----
    print("=" * 60)
    print("Test 3: 奇偶中位数验证")
    print("=" * 60)

    # 偶数个
    mf3 = MedianFinder()
    for x in [1, 2, 3, 4]:
        mf3.addNum(x)
    print(f"  [1,2,3,4] -> 中位数 = {mf3.findMedian()}  (期望 2.5)")

    # 奇数个
    mf3.addNum(5)
    print(f"  [1,2,3,4,5] -> 中位数 = {mf3.findMedian()}  (期望 3.0)")

    # ---- test 4: 重复数字 ----
    print()
    print("=" * 60)
    print("Test 4: 重复数字")
    print("=" * 60)
    mf4 = MedianFinder()
    for _ in range(99):
        mf4.addNum(7)
    mf4.addNum(9)
    print(f"  99个7, 1个9 -> 中位数 = {mf4.findMedian()}  (期望 7.0)")
    mf4.addNum(9)
    print(f"  再加1个9  -> 中位数 = {mf4.findMedian()}  (期望 7.0)")

    print()
    print("全部测试完成")
