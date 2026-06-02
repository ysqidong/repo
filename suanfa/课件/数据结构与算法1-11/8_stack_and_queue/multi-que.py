import multiprocessing
import time


def worker(task_queue, result_queue):
    """工作进程：从任务队列取任务，计算平方后把结果放入结果队列"""
    while True:
        try:
            # 获取任务（阻塞等待，超时1秒）
            x = task_queue.get(timeout=1)
            if x is None:  # 收到结束信号
                break

            # 模拟一些计算耗时
            time.sleep(0.1)

            # 计算平方
            result = x ** 2
            result_queue.put((x, result))

        except:
            break


def main():
    # 创建任务队列和结果队列
    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # 准备10个任务：计算 0~9 的平方
    tasks = list(range(10))

    # 把任务放入队列
    for t in tasks:
        task_queue.put(t)

    # 启动3个工作进程
    num_workers = 3
    processes = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(task_queue, result_queue))
        p.start()
        processes.append(p)
        # 发送结束信号（每个进程一个）
        task_queue.put(None)

    # 收集结果
    results = []
    for _ in tasks:
        x, result = result_queue.get()
        results.append((x, result))
        print(f"{x}² = {result}")

    # 等待所有进程结束
    for p in processes:
        p.join()

    print(f"\n所有任务完成！共 {len(results)} 个结果")


if __name__ == "__main__":
    main()