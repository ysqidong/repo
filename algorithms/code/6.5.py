import heapq

class MedianFinder:
    def __init__(self):
        # 大顶堆：存较小的一半（用负数模拟）
        self.max_heap = []
        # 小顶堆：存较大的一半
        self.min_heap = []
    
    def addNum(self, num: int) -> None:
        # 1. 决定加到哪个堆
        if not self.max_heap or num <= -self.max_heap[0]:
            # 加到左半边（大顶堆）
            heapq.heappush(self.max_heap, -num)
        else:
            # 加到右半边（小顶堆）
            heapq.heappush(self.min_heap, num)
        
        # 2. 保持平衡：两堆大小之差不超过1，且 max_heap 不少于 min_heap
        if len(self.max_heap) > len(self.min_heap) + 1:
            # 把 max_heap 的最大元素移到 min_heap
            moved = -heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, moved)
        elif len(self.min_heap) > len(self.max_heap):
            # 把 min_heap 的最小元素移到 max_heap
            moved = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -moved)
    
    def findMedian(self) -> float:
        # 总数为奇数：返回大顶堆的堆顶
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        # 总数为偶数：返回两个堆顶的平均值
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0
mf = MedianFinder()
mf.addNum(3)      # 堆：max=[-3], min=[]
print(mf.findMedian())  # 3.0

mf.addNum(1)      # 添加后：max=[-1], min=[3]
print(mf.findMedian())  # (1+3)/2 = 2.0

mf.addNum(4)      # 添加4→max=[-3], min=[1,4]? 平衡后：max=[-1], min=[3,4]
# 实际过程：4>1进min=[3,4]→len(min)2>len(max)1→移3到max→max=[-3,-1], min=[4]
print(mf.findMedian())  # -max[0]=3，即 3.0

mf.addNum(1)      # 添加：max=[-3,-1,-1], min=[4]? 平衡后：max=[-1,-1], min=[3,4]
print(mf.findMedian())  # (1+3)/2 = 2.0

mf.addNum(5)      # 添加：max=[-1,-1], min=[3,4,5]? 平衡后：max=[-3,-1], min=[4,5]
print(mf.findMedian())  # max[0]=-3 → 3.0
'''时间复杂度
操作	时间复杂度	说明
addNum()	O(log n)	每次 push/pop 堆操作 O(log n)，常数次
findMedian()	O(1)	只返回堆顶元素
空间复杂度
O(n)：存储所有添加的元素'''