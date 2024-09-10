  > https://docs.python.org/3/library/multiprocessing.html

## 1 The Process class

### 1.1 Process class Description

**==processing==**
A **process** is the basic unit of resource allocation[](资源分配) and scheduling in an operating system, representing an independent program executing on a specific data set.
Processes are the foundation of operating system architecture; in early process-oriented computer designs, they were the basic execution entity for programs. In contemporary thread-oriented computer designs, processes serve as containers for threads. A process requires certain system resources, such as CPU time, memory space, files, and input/output devices, to complete its tasks.

**==multiprocessing VS multithreading==**
Due to the presence of the GIL (Global Interpreter Lock), when using multithreading, operations can only occur on a single CPU, preventing the use of multiple CPU capabilities.
Using multiprocessing allows you to take advantage of multiple CPUs for concurrent operations, improving execution efficiency:

- **Multi-CPU operations** should use multiprocessing (e.g., for computations, image processing).
- **I/O-bound operations** should use multithreading.
- The overhead of thread switching is significantly lower than that of process switching, so multithreading should be prioritized.


**==multiprocessing module function==**

| No. | Function                                                              | Description                                                                                                                                                     |
| --- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Process(target=None, name=None, args=(), kwargs={}, *, daemon=None)` | create Process objects                                                                                                                                          |
| 2   | `run()`                                                               | Method representing the process’s activity                                                                                                                      |
| 3   | `start()`                                                             | Start the process’s activity                                                                                                                                    |
| 4   | `join([_timeout_])`                                                   | thread wait until the called process terminates.  <br>if the `timeout` argument is specified，main process will block for specified time for run called process. |
| 5   | `name`                                                                | The process’s name                                                                                                                                              |
| 6   | `is_alive()`                                                          | Return whether the process is alive.                                                                                                                            |
| 7   | `daemon`                                                              | The process’s daemon flag, a Boolean value                                                                                                                      |
| 8   | `pid`                                                                 | Return the process ID                                                                                                                                           |
| 9   | `terminate()`                                                         | Terminate the process. On POSIX this is done using the SIGTERM signal                                                                                           |
| 10  | `kill()`                                                              | Same as terminate() but using the SIGKILL signal on Unix.                                                                                                       |
| 11  | `close()`                                                             | close object and releasing all resources associated with it.                                                                                                    |


### 1.2 Create Process object

Two basic way to create
* Create object by  `Process` contributor in `multiprocessing` module 
* Create object by Class which inherting from `Process` Class

```python
from multiprocessing import Process, current_process 
import time

""" 
    The First use script of Process : `Process` Class Contributor
    1 Get current process pid and name by current_process() in multiprocessing module
    2 Know what is Main Process or Sub Process
    3 Create process object by `Process` Class in `multiprocessing` module 
    4 Define the thread execution logic function and start the thread. 
    5 Use a list to manage threads
"""

def process_core(delay, count):       # Simulate the processing of core business functions
    for num in range(count):
        # output process info, pid & name
        print("【count = %d】Process ID : %s , Process Name : %s execute .... " % 
              (num, current_process().pid, current_process().name))
        time.sleep(delay)

def main():
    # Main Process
    print("【Main】Process ID : %s , Process Name : %s execute ...." % 
            (current_process().pid, current_process().name))
    print()
    # Sub Process
    process_arr = []
    for item in range(3):
        p = Process(
            target=process_core, 
            args=(1, 5,),
            name=f"core business - {item}"
        )
        p.start()
        process_arr.append(p)
    for p in process_arr:
        p.join()

if __name__ == '__main__':
    main()

```

```python
from multiprocessing import Process, current_process 
import time

""" 
    The Second use script of Process : Inhreting from Process Class
    1 Create process object by inheriting from `Process` Class 
    2 Customize the attributes of the process object in __init__()
    3 Define the process execution logic function run()
    4 Create a custom process object and start it
"""

class ExecCoreBusiness(Process): 
    def __init__(self, **kwargs):
        super().__init__(name=kwargs.get('name'))
        self.__delay = kwargs.get('delay')
        self.__count = kwargs.get('count')

    def run(self):                             # Defines the business logic
        for num in range(self.__count):
        # output process info, pid & namd
            print("【count = %d】Process ID : %s , Process Name : %s execute .... " % 
                (num, current_process().pid, current_process().name))
            time.sleep(self.__delay)

def main():
    # Main Process
    print("【Main】Process ID : %s , Process Name : %s execute ...." % 
            (current_process().pid, current_process().name))
    print()
    # Sub Process
    process_arr = []
    for item in range(3):
        p = ExecCoreBusiness(                       # Create Object by Custom Process Class
            name = f'core business - {item}', 
            delay = 2,
            count = 5
        )
        p.start()
        process_arr.append(p) 
    for p in process_arr:
        p.join()

if __name__ == '__main__':
    main()

```

### 1.3 Process Control

| No. | Function             | Description                    |
| --- | -------------------- | ------------------------------ |
| 1   | `start()`            | 使进程进入就绪状态，会等待有资源时才启动           |
| 2   | `terminate()`        | 关闭进程(发送SIGTERM信号)，具体状态可以通过程序捕捉 |
| 3   | `is_alive()`         | 查看进程是否存活                       |
| 4   | `join(timeout=None)` | 强制运行进程（可以设置超时时间）               |
| 5   | `kill()`             | 关闭进程（发送SIGKILL信号），彻底结束进程运行     |
```python
from multiprocessing import Process, current_process 
import time

""" 
    The Third use script of Process : s001_simple_multiprocessing03.py
    1 join()
    2 is_alive()
    3 terminate()
    4 kill()
"""


def process_core(id, delay):
    time.sleep(delay)
    print("【Sub Process %d】Process ID : %s , Process Name : %s execute .... " % 
            (id, current_process().pid, current_process().name))

def main():
    
    # If p.join() is called, the "Sub Process" will be executed first. If p.join() is not called, "Main Process End" will be executed first, followed by the "Sub Process."
    print("【Main Process 1】Process ID : %s , Process Name : %s start ...." % 
            (current_process().pid, current_process().name))
    print()
    # Sub Process
    p = Process(                
            name = f'core business', 
            target=process_core,
            args=(1,1,)
        )
    p.start()
    p.join()
    print()
    print("【Main Process 1】Process ID : %s , Process Name : %s End ...." % 
            (current_process().pid, current_process().name))
    
    print('######################################################################')
    # Before if is_alive judgement, p2 run finish. So if logic won't execute.
    print("【Main Process 2】Process ID : %s , Process Name : %s start ...." % 
            (current_process().pid, current_process().name))
    print()
    # Sub Process
    sleep_second = 2
    p_sleep_second = 1
    p2 = Process(                
            name = f'core business', 
            target=process_core,
            args=(2,p_sleep_second,)
        )
    p2.start()
    time.sleep(sleep_second)
    if p2.is_alive():              # no , so not execute
        p2.terminate()
        print('After %d second(s) , %s is still alive. but now %s Process will Terminate.' % 
              (sleep_second, p2.name, p2.name))
    print()
    print("【Main Process 2】Process ID : %s , Process Name : %s End ...." % 
            (current_process().pid, current_process().name))
    
    print('######################################################################')
    # Before if is_alive judgement, p2 not finish. So if logic will be execute.
    print("【Main Process 3】Process ID : %s , Process Name : %s start ...." % 
            (current_process().pid, current_process().name))
    print()
    # Sub Process
    sleep_second = 1
    p_sleep_second = 2
    p2 = Process(                
            name = f'core business', 
            target=process_core,
            args=(3,p_sleep_second,)
        )
    p2.start()
    time.sleep(sleep_second)
    if p2.is_alive():              # yes , so p2 will be terminate and not execute
        p2.terminate()
        print('After %d second(s) , %s is still alive. but now %s Process will Terminate.' % 
              (sleep_second, p2.name, p2.name))
    print()
    print("【Main Process 3】Process ID : %s , Process Name : %s End ...." % 
            (current_process().pid, current_process().name))
    
    print('######################################################################')
    # Before if is_alive judgement, p2 not finish. So if logic will be execute.
    print("【Main Process 3】Process ID : %s , Process Name : %s start ...." % 
            (current_process().pid, current_process().name))
    print()
    # Sub Process
    sleep_second = 1
    p_sleep_second = 2
    p2 = Process(                
            name = f'core business', 
            target=process_core,
            args=(3,p_sleep_second,)
        )
    p2.start()
    time.sleep(sleep_second)
    if p2.is_alive():              # it's alive now, so p3 will be terminate and won't print info
        p2.kill()
        print('After %d second(s) , %s is still alive. but now %s Process will Terminate.' % 
              (sleep_second, p2.name, p2.name))
    print()
    print("【Main Process 3】Process ID : %s , Process Name : %s End ...." % 
            (current_process().pid, current_process().name))
    
if __name__ == '__main__':
    main()

```

### 1.4 Daemon

在进程执行过程之中，如果某一个进程启动了，那么一般都是执行到完，但是也可以由另外的一个进程来进行结束的处理。
在一个 Python 应用过程之中，每一个进程启动都意味着要配置其处理的业务逻辑(业务子进程)，但是某些进程在执行的时候可能需要其他进程的帮助。例如:富豪的生活里面是需要有仆人的，仆人为其穿衣服，，为其喂饭，为其拿手机。
在操作系统里面，也可以针对于某一个进程来设置一些辅助的进程，而这样的进程就称为守护进程。


Suppose we want to implement a data chat feature, but we need to archive each chat record. Therefore, we can write a daemon process that asynchronously uploads each sent message to the server, enabling employee monitoring.
```python
from multiprocessing import Process, current_process 
import time

""" 
    The fifth use script of Process : s002_simple_multiprocessing03.py
    1 Daemon , create daemon and start by called process. when called process end, daemon process alse will disapper 
"""


def process_core():           # core business
    # create daemon and start by called process. when called process end, daemon process alse will disapper 
    daemon_p = Process(target=process_check, name='daemon_process', daemon=True) # Daemon set True
    daemon_p.start()
    # process of core business
    for item in range(2):
        print('【Sub Process】Process ID : %s , Process Name : %s , Current Stage: %d / 2' %
            (current_process().pid, current_process().name, item+1))
        time.sleep(2)
    print('【Sub Process】Process ID : %s , Process Name : %s , End' %   
                (current_process().pid, current_process().name))

def process_check():           # check process 
    count = 1
    while True:                # keep check
        print('【Daemon %s】The %d-th check' % (current_process().name ,count))
        count += 1
        time.sleep(1)
    
def main():
    p = Process(target=process_core, name='Core Business Process')
    p.start()
    time.sleep(10)
    print('【Main Process】Process ID : %s , Process Name : %s End' %
        (current_process().pid, current_process().name))
if __name__ == '__main__':
    main()
```

## 2 Exchanging objects between processes

   > communication between processes

When using multiple processes, one generally uses **message passing** for communication between processes and avoids having to use any synchronization primitives like locks.
There are two message passing tools:
* `Pipe()` :  (for a connection between two processes, `Pipe` has higher performance than `Queue`) 
* `queue` :  (which allows multiple producers and consumers)

### 2.1 Pipe Description

* `multiprocessing.Pipe()` is function, returns a pair `(conn1, conn2)` of `Connection` objects representing the ends of a pipe

| No. | Function           | Description                                                                                                                                                                                                                                                |
| --- | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Pipe([duplex])`   | Return (conn1, conn2) of `Connection` objects tuple,<br>If _duplex_ is `True` (default) then the pipe is bidirectional[](双向)<br>If _duplex_ is `False` then the pipe is unidirectional[](单向): `conn1` only can receive messages and `conn2` only can send. |

* `multiprocessing.connection.Connection` 
	* "Picklable" refers to an object that can be serialized and deserialized.

| No. | Function    | Description                                                                                                                                                                  |
| --- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `send(obj)` | Send an object to the other end of the connection which should be read using `recv()`.<br>The object must be picklable. Very large pickles (32 MiB+) may raise a ValueError. |
| 2   | `recv()`    | Return an object sent from the other end of the connection using send()                                                                                                      |
| 3   | `close()`   | Close the connection.This is called automatically when the connection is garbage collected.                                                                                  |

### 2.2 Pipe Case

```python
from multiprocessing import Process, Pipe

def worker(conn):
    conn.send("Hello, world!")        # Send data to the other end of the pipe
    conn.close()                      # Close the connection

# Create a pipe
parent_conn, child_conn = Pipe()

# Create a new process
p = Process(target=worker, args=(child_conn,))

# Start the new process
p.start()

# Receive data from the pipe
print(parent_conn.recv())               # Outputs: "Hello, world!"

# Wait for the process to finish
p.join()
```

### 2.3 Queue Description

You cannot use `queue.Queue` in multiprocessing programming. Instead, you should use `multiprocessing.Queue`
Queue has servel type:
* `multiprocessing.Queue` :  It provides thread-safe queue operations. It can be used in a multithreaded environment to achieve inter-thread communication and data exchange using pipes and locks.。
* `multiprocessing.JoinableQueue` : It includes additional methods such as `task_done()` and `join()`, which are used to notify that a task in the queue has been completed.⭐

| No. | Function                       | Description                                                                                                                                                                                                                                                                                                                                                                |
| --- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Queue([maxsize])`             | If _maxsize_ is less than or equal to zero, the queue size is infinite                                                                                                                                                                                                                                                                                                     |
| 2   | `get([block[, timeout]])`      | if _block_ is `True` (the default) : <br>- `get(True)` `get()` : it will block until an item is available<br>- `get(True,timeout)` : it will blocks at most _timeout_ seconds then raise `queue.Empty exception`<br>if _block_ is `False` :   `get(False)`, `get(False, 3487)`<br>- return an item if one is immediately available, else raise the `queue.Empty exception` |
| 3   | `put(obj[, block[, timeout]])` | `put` and `get` are similar:<br>- `get` checks whether the `Queue` has tasks and if it can retrieve a task from it.<br>- `put` checks whether there is room in the `Queue` and if it can insert a task into it.                                                                                                                                                            |
| 4   | `empty()`                      | Return `True` if the queue is empty, but it is not reliable because of multithreading/multiprocessing                                                                                                                                                                                                                                                                      |
| 5   | `qsize()`                      | Return the approximate size of the queue.  not reliable                                                                                                                                                                                                                                                                                                                    |
| 6   | `full()`                       | Return `True` if the queue is full, `False` otherwise. not reliable                                                                                                                                                                                                                                                                                                        |

| No. | Function                   | Description                                                                                                                                                                                                                                                                |
| --- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `JoinableQueue([maxsize])` | If _maxsize_ is less than or equal to zero, the queue size is infinite                                                                                                                                                                                                     |
| 2   | `task_done()`              | When a consumer thread retrieves a task from the JoinableQueue using `get()`, it should call the `task_done()` method to indicate that the task has been completed. This informs the `JoinableQueue` that the data item originally placed in the queue has been processed. |
| 3   | `join()`                   | Block until all items in the queue have been gotten and processed.                                                                                                                                                                                                         |
### 2.4 Queue Case

```python
from multiprocessing import Process, Queue

def producer(queue):
    for i in range(5):
        print('Producer putting data')
        queue.put(i)
        print('Producer done')

def consumer(queue):
    while not queue.empty():
        data = queue.get()
        print('Consumer got data', data)

# Create a shared queue
queue = Queue()

# Create the producer and consumer processes
producer_process = Process(target=producer, args=(queue,))
consumer_process = Process(target=consumer, args=(queue,))

# Start the processes
producer_process.start()
producer_process.join()  # Wait for the producer to finish

consumer_process.start()
consumer_process.join()  # Wait for the consumer to finish
```

### 2.5 JoinableQueue Case

```python
from multiprocessing import Process, JoinableQueue
import random
import time

def task_generator(queue):
    for i in range(10):
        print(f"Generator: generating task {i}")
        queue.put(i)
    queue.join()                          # Wait for all tasks to be completed
    print("Generator: all tasks completed.")

def worker(queue):
    while True:
        task = queue.get()                # get and remove task from queue
        print(f"Worker {Process.current_process().name}: starting task {task}")
        time.sleep(random.randint(1, 3))  # Simulate time to complete the task
        print(f"Worker {Process.current_process().name}: finished task {task}")
        queue.task_done()                 # use task_done() to tell queue this task is finis

# Create a queue
queue = JoinableQueue()

# Create the task generator process
generator = Process(target=task_generator, args=(queue,))

# Create worker processes
workers = [Process(target=worker, args=(queue,)) for _ in range(3)]

# Start the generator and workers
generator.start()
for worker in workers:
    worker.start()

# Wait for all processes to finish
generator.join()
for worker in workers:
    worker.terminate()
```

## 3 Sharing state between processes

Although shared state is necessary in some cases, it is generally better to avoid it whenever possible and utilize other concurrency patterns, such as message passing, event-driven architectures, or task queues. In Python, there are several libraries and tools, such as `queue.Queue`, `multiprocessing.Pool`, and `concurrent.futures`, that can help you implement these concurrency patterns without directly managing shared state.

* **Shared memory**
	* [`Value`](https://docs.python.org/3.11/library/multiprocessing.html#multiprocessing.Value "multiprocessing.Value") or [`Array`](https://docs.python.org/3.11/library/multiprocessing.html#multiprocessing.Array "multiprocessing.Array")
* **Server process**
	* [`Manager()`](https://docs.python.org/3.11/library/multiprocessing.html#multiprocessing.Manager "multiprocessing.Manager")

### 3.2 Manager

```python
from multiprocessing import Process, Manager 
import time

""" 
    Manager().dict() can share between processes. If in multiprocess , you should use Synchronization primitives(RLock, condition ...) to ensure process safety.
"""

def add_data(p_dict, key, value):
    p_dict[key] = value

def main():
    process_dict = Manager().dict()

    p_1 = Process(target=add_data, args=(process_dict, 'p_1', 11))
    p_2 = Process(target=add_data, args=(process_dict, 'p_2', 12))
    p_1.start()
    p_2.start()
    p_1.join()
    p_2.join()
    # first , update process_dict in each process
    # secound, print process_dict in main process
    print(process_dict)   # {'p_1': 11, 'p_2': 12}

if __name__ == '__main__':
    main()

```

## 4 Synchronization primitives

| No. | Function                                                      | Description                                 |
| --- | ------------------------------------------------------------- | ------------------------------------------- |
| 1   | `multiprocessing.Barrier(_parties_[, _action_[, _timeout_]])` | The usage is similar to that of `threading` |
| 2   | `multiprocessing.BoundedSemaphore([_value_])`                 | ......                                      |
| 3   | `multiprocessing.Condition([_lock_])`                         | ......                                      |
| 4   | `multiprocessing.Event`                                       | ......                                      |
| 5   | `multiprocessing.Lock`                                        | ......                                      |
| 6   | `multiprocessing.RLock`                                       | ......                                      |
| 7   | `multiprocessing.Semaphore([_value_])`                        | ......                                      |


## 5 Pool

### 5.1 Pool Description

`multiprocessing.pool.Pool`
The so-called "XX pool" refers to the unified management of resources[](对资源的统一管理). 
If an operating system allows for an unlimited number of processes to be spawned[](产生 spawned, 无限制的增加进程), it will inevitably[](不可避免地) affect the execution speed of other processes. 
To ensure that processes remain within a reasonable range of server hardware resources, it is necessary to effectively control the number of processes, which can be achieved through the use of a process pool. 
It is generally recommended that the number of processes in the pool matches the number of CPU cores.

**==multiprocessing.pool.Pool==**

| No. | Function                                                                                                       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `multiprocessing.pool.Pool(`<br>`[processes[, initializer[, initargs[, maxtasksperchild[, context]]]]]`<br>`)` | `processes` : the number of worker processes(default `os.cpu_count()`)<br>`initializer` & `initargs`: the initialization function and its parameters                                                                                                                                                                                                                                                                                                                      |
| 2   | `apply(func[, args[, kwds]])`                                                                                  | Synchronously execute threads, where the threads call a specified func and args <br>`func` : call function<br>`args` : function parameters                                                                                                                                                                                                                                                                                                                                |
| 3   | `apply_async(func[, args[, kwds[, callback[, error_callback]]]])`                                              | Asynchronous execution threads, where the threads call a specified func and args. Return AsyncResult means can obtain the return result or any error information returned<br>`callback` : callback func need accepts a single argument(rst). It will be called when no exeception occur.<br>`error_callback` : error_callback func accepts a single argument(err). It will be called when exeception occur.                                                               |
| 4   | `map(func, iterable[, chunksize])`                                                                             | Synchronously execute threads, where the threads call a specified func and each chunk as args <br>`func` : call function<br>`iterable` : will be split into multiple chunks, each chunk will be submitted to a process<br>`chunksize` : the size of each chunk(default )                                                                                                                                                                                                  |
| 5   | `map_async(func, iterable[, chunksize[, callback[, error_callback]]])`                                         | A variant of the map() method which returns a AsyncResult object.<br>Asynchronous execute threads, where the threads call a specified func and each chunk as args. Return AsyncResult means can obtain the return result or any error information returned<br>`callback` : function which accepts a single argument. it will be called when no exeception occur.<br>`error_callback` : function which accepts a single argument. it will be called when exeception occur. |
| 6   | `imap(func, iterable[, chunksize])`                                                                            | A lazier version of `map()`                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|     | `imap_unordered(func, iterable[, chunksize])`                                                                  | The same as `imap()` except that the ordering of the results from the returned iterator                                                                                                                                                                                                                                                                                                                                                                                   |
| 7   | `close()`                                                                                                      | Prevents any more tasks from being submitted to the pool[](不再向池提交task). **Continue completing outstanding work**[](完成未完成工作)，Once[](一旦) all the tasks have been completed the worker processes will exit.                                                                                                                                                                                                                                                                  |
| 8   | `terminate()`                                                                                                  | Stops the worker processes immediately **without completing outstanding work.**                                                                                                                                                                                                                                                                                                                                                                                           |
| 9   | `join()`                                                                                                       | **Wait for all worker processes finish then exit**. <br>**Must call close() or terminate() before using join().**                                                                                                                                                                                                                                                                                                                                                         |

**==multiprocessing.pool.AsyncResult==** : the result returned by `Pool.apply_async()` and `Pool.map_async()`.

| No. | Function            | Description                                                                                                                                                 |
| --- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `get([_timeout_])`  | Return the result of callback or error_callback func when it arrives. If timeout is specified and exceeds time limit, return `multiprocessing.TimeoutError` |
| 2   | `wait([_timeout_])` | Wait until the result is available or until _timeout_ seconds pass.                                                                                         |
| 3   | `ready()`           | Return whether the call has completed.                                                                                                                      |
| 4   | `successful()`      | Return whether the call completed without raising an exception.                                                                                             |

### 5.2 Pool Case

#### 5.2.1 apply

If you have a large number of tasks to submit and do not need to retrieve the results immediately[](立即获取结果), using the `apply_async()` method can provide better performance.

```python
from multiprocessing import Pool
import time
def square(x):
	time.sleep(3)
    return x * x

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        # use apply()
        result = pool.apply(square, (2,))
        print(result)  # 输出: 4

        # use apply_async()
        result_obj = pool.apply_async(square, (3,))
        # wait all task finish
        pool.close()
        pool.join()
        # task finish, you can get result
        print(result_obj.get())  # 9
```

#### 5.2.2 map

```python
import time
from multiprocessing import Pool

# 一个需要大量计算的函数
def expensive_computation(x):
    sum([i*i for i in range(1000000)])
    return x * x

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        # use map
        start_time = time.time()
        result_sync = pool.map(expensive_computation, range(10))
        elapsed_time_sync = time.time() - start_time

        # use map_async 
        start_time = time.time()
        result_obj = pool.map_async(expensive_computation, range(10, 20))
        # use get() to get Async result
        result_async = result_obj.get()
        elapsed_time_async = time.time() - start_time

    print(f"Synchronous execution time: {elapsed_time_sync}")
    print(f"Asynchronous execution time: {elapsed_time_async}")
```


#### 5.2.3 imap

```python
from multiprocessing import Pool

def square(x):
    return x * x

if __name__ == "__main__":
    with Pool(processes=4) as pool:
        # map return list
        results = pool.map(square, range(10))            
        print("map results:", results)

        # lazy version imap return iterator[](可迭代对象)
        results = pool.imap(square, range(10, 20))
        print("imap results:", list(results))

        # lazy version imap_unordered return iterator
        results = pool.imap_unordered(square, range(20, 30))
        print("imap_unordered results:", list(results))
```

