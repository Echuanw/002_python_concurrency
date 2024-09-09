"""
Use Function And Attribute of Barrier
这个例子中，我们创建了一个`Barrier`对象和三个线程。线程在`Barrier`对象上等待，当所有线程都调用了`wait()`方法后，它们都会被解除阻塞。
然后，线程检查它的`worker_id`，如果`worker_id`是0（也就是说，这个线程是最后一个到达屏障的线程），那么它会重置屏障，让所有线程再次等待。
如果`Barrier`对象在被重置时有线程正在等待，那么这些线程会收到一个`BrokenBarrierError`异常。
"""
import threading
import time

# thread function logic and receive a barrier object
def worker(barrier):
    while True:
        print("【Opt 1】 ", threading.current_thread().name, "waiting for barrier with {} others ".format(barrier.parties - barrier.n_waiting))
        try:
            worker_id = barrier.wait()          
        except threading.BrokenBarrierError:
            print('receive `BrokenBarrierError`')
            break
        print("【Opt 2】 ", threading.current_thread().name, "after barrier", worker_id)
        if worker_id == 0:
            # reset the barrier
            time.sleep(10)
            barrier.reset()
            

barrier = threading.Barrier(3)  

for i in range(3):
    threading.Thread(name='worker-%s' % (i + 1), target=worker, args=(barrier,)).start()