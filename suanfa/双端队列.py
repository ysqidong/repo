"""from collections import deque
dq=deque([1,2,3,4,5])
dq.append(6)
print(dq)
dq.appendleft(0)
print(dq)
dq.pop()
dq.popleft()
print(dq)"""
import multiprocessing
import time


def worker(task_queue, result_queue):
    while True:
        try:
            x = task_queue.get(timeout=1)
        except :
            break
        if x is None:
            break
        time.sleep(0.1)
        result_queue.put(x * x)


def main():
    task_quene = multiprocessing.Queue()
    result_quene = multiprocessing.Queue()
    for i in range(10):
        task_quene.put(i)
    processes = []
    for _ in range(4):
        p = multiprocessing.Process(target=worker, args=(task_quene, result_quene))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    results = []
    while not result_quene.empty():
        results.append(result_quene.get())
    print(results)
if __name__ == "__main__":
    main()