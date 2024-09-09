import threading
import time
import random

# 创建一个线程局部数据对象
local_data = threading.local()

def worker():
    # 在当前线程的命名空间中，给mydata对象的x属性赋值
    if not hasattr(local_data, 'task_count'):
        local_data.task_count = 0

    for i in range(100):
        local_data.task_count += 1
        if i % 10 == 0:
            print(f"{threading.current_thread().name} load : {i} / 100")
        time.sleep(random.random())

    print(f"{threading.current_thread().name} finished with task count: {local_data.task_count}")

# 创建两个线程
thread1 = threading.Thread(target=worker)
thread2 = threading.Thread(target=worker)

thread1.start()
thread2.start()

thread1.join()
thread2.join()