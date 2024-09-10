
## 1 threading module function

| No. | Function           | Description                                           |
| --- | ------------------ | ----------------------------------------------------- |
| 1   | `active_count()`   | Return the number of Thread objects currently alive   |
| 2   | `current_thread()` | Return the current Thread objects                     |
| 3   | `main_thread()`    | Return the main thread                                |
| 4   | `get_ident()`      | Return the ‘thread identifier’ of the current thread. |

```python
"""
Use case of module function
"""
import threading 
def worker(): 
    if threading.current_thread() == threading.main_thread():
        print("【On main thread】")
    else:
        print("【Not on main thread】")
    print(f"Worker thread is: {threading.current_thread().name}")             # MainThread  |  Thread-1 (worker)
    print(f"Active threads: {threading.active_count()}")                      # 1           |  2
    print(f"Worker thread id: {threading.get_ident()}")

# main
worker()
print("#################################################################")
# new thread
thread= threading.Thread(target=worker) 
thread.start()
```

## 2 Thread-Local Data

Threads have their own data, which is managed by the `threading.local` class. You can store data using attributes.
Thread local data provides an independent storage space for each thread, so that each thread can store and modify its own state information independently without affecting other threads. 

Although they appear to[](看起来) be operating on the same data, they are actually manipulating copies[](操作副本) of their own thread-local data. Therefore, both threads will print 2 instead of 3.
```python
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
```

## 3 Thread Objects

### 3.1 `threading.Thread` Class Description

| No. | Structure                                                                 | type        | Desciption                                                                                                                                                                           |
| --- | ------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Thread(_target=None_, _name=None_, _args=()_, _kwargs={}_, _daemon=None_) | constructor | `target` : the callable object to be invoked by the `run()` method<br>`name` : the thread name<br>`args` : a list or tuple of arguments<br>`daemon` : whether the thread is daemonic |
| 2   | start()                                                                   | func        | Start the thread’s activity, then thread will execute `run()`                                                                                                                        |
| 3   | run()                                                                     | func        | thread’s activity method                                                                                                                                                             |
| 4   | join(_timeout=None_)                                                      | func        | main thread wait until the called thread terminates.  <br>if the `timeout` argument is specified，main thread will block for specified time for run called thread.                    |
| 5   | is_alive()                                                                | func        | whether the thread is alive, **True or False**                                                                                                                                       |
| 6   | name                                                                      | attribute   | thread name                                                                                                                                                                          |
| 7   | native_id                                                                 | attribute   | The Thread ID (**TID**) of this thread                                                                                                                                               |
| 8   | daemon                                                                    | attribute   | A boolean value indicating whether this thread is a daemon thread (`True`) or not (`False`).                                                                                         |

### 3.2 Case of Create And Start

**Recommend Thread object by Thread Contributor**

```python
from threading import Thread, current_thread
import time

""" 
    The First use script of Thread 
    1 Thread Attribute : native_id, name, daemon
    2 Create Thread object by Thread Contributor [recommend]
    3 Create Thread object by inhert Thread Class
"""

def thread_core(delay, count):
    """Simulate the Threading of core business functions"""
    for num in range(count):
        # output Thread info, id & name
        print("【count = %d】Thread ID : %s , Thread Name : %s , This thread is Daemon Thread ? %s ,execute .... " % 
              (num, current_thread().native_id, current_thread().name, current_thread().daemon))
        time.sleep(delay)


class SubThreadForCoreBusiness(Thread): 
    """Create thread by inhert Thread Class"""
    def __init__(self, **kwargs):
        super().__init__(name=kwargs.get('name'))
        self.__delay = kwargs.get('delay')
        self.__count = kwargs.get('count')

    def run(self):                             # Defines the business logic
        for num in range(self.__count):
        # output process info, pid & namd
            print("【count = %d】Thread ID : %s , Thread Name : %s , This thread is Daemon Thread ? %s ,execute .... " % 
                (num, current_thread().native_id, current_thread().name, current_thread().daemon))
            time.sleep(self.__delay)

def main():
    ##############################################################################
    # 1 Thread Attribute : native_id, name, daemon
    print("【Main】Thread ID : %s , Thread Name : %s , This thread is Daemon Thread ? %s ,execute ...." % 
            (current_thread().native_id, current_thread().name, current_thread().daemon))
    print()
    ##############################################################################
    # 2 Create Thread object by Thread Contributor
    thread_arr1 = []
    for item in range(3):
        p = Thread(
            target=thread_core, 
            args=(1, 5,),
            name=f"core business - {item}"
        )
        p.start()
        thread_arr1.append(p)
    for p in thread_arr1:
        p.join()
    print()
    ##############################################################################
    # 3 Create Thread object by Thread Contributor
    thread_arr2 = []
    for item in range(3):
        p = SubThreadForCoreBusiness(
            name=f"Sub core business - {item}",
            delay = 1,
            count = 3
        )
        p.start()
        thread_arr2.append(p)
    for p in thread_arr2:
        p.join()
    print()

if __name__ == '__main__':
    main()
```

### 3.3 Case of Daemon

   > Daemon , create daemon and start by called thread. when called thread end, daemon thread alse will disapper

```python
from threading import Thread, current_thread
import time

""" 
    The Second use script of Thread
    1 Daemon , create daemon and start by called thread. when called thread end, daemon thread alse will disapper 
"""

def thread_core():           # core business
    # create daemon and start by called thread. when called thread end, daemon thread alse will disapper 
    daemon_p = Thread(target=thread_check, name='daemon_thread', daemon=True) # Daemon set True
    daemon_p.start()
    # thread of core business
    for item in range(2):
        print('【Sub Thread】Thread ID : %s , Thread Name : %s , This thread is Daemon Thread ? %s , Current Stage: %d / 2' %
            (current_thread().native_id, current_thread().name, current_thread().daemon, item+1))
        time.sleep(2)
    print('【Sub Thread】Thread ID : %s , Thread Name : %s , This thread is Daemon Thread ? %s , End' %   
                (current_thread().native_id, current_thread().name, current_thread().daemon))

def thread_check():           # check thread 
    count = 1
    while True:                # keep check
        print('【Daemon %s】The %d-th check, This thread is Daemon Thread ? %s' % (current_thread().name ,count, current_thread().daemon))
        count += 1
        time.sleep(1)
    
def main():
    p = Thread(target=thread_core, name='Core Business Thread')
    p.start()
    time.sleep(10)
    print('【Main Thread】Thread ID : %s , Thread Name : %s , This thread is Daemon Thread ? %s ,End' %
        (current_thread().native_id, current_thread().name, current_thread().daemon))
if __name__ == '__main__':
    main()

```

## 4 Lock & RLock Objects

### 4.1 Lock & RLock Description

`threading.Lock` Class Description. 
When multiple threads share the same resource (variable), it can lead to unpredictable[](不可控) results, potentially[](可能) causing the program to fail or crash. 
We can use locks to protect the same resource. **Only the thread that acquires the lock[](获得锁) can access this resource**, while other threads that do not have the lock will be blocked until the thread that holds the lock releases it. 

| No. | Structure   | type         | Desciption                                                                                                            |
| --- | ----------- | ------------ | --------------------------------------------------------------------------------------------------------------------- |
| 1   | Lock()      | factory func | returns an instance of the lock                                                                                       |
| 2   | acquire()   | func         | Acquire a lock then thread can access resource.                                                                       |
| 3   | release()   | func         | Release a lock then other thread can acquire this lock.                                                               |
| 4   | locked()    | func         | Return `True` if the lock is acquired                                                                                 |
| 5   | with _lock: | use way      | locks also support the context management protocol.the `with` statement automatically acquires and releases the lock. |

`threading.RLock` Class Description.
The basic behavior of `RLock` in Python is similar to that of `Lock`, with the difference being that a `Lock` can only be acquired once by the same thread, while an `RLock` can be acquired multiple times by the same thread.

| No. | Structure    | type         | Desciption                                                                                                                       |
| --- | ------------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| 1   | RLock()      | factory func | returns an instance of the reentrant lock                                                                                        |
| 2   | acquire()    | func         | Acquire a lock，                                                                                                                  |
| 3   | release()    | func         | Release a lock                                                                                                                   |
| 5   | with _rlock: | use way      | Reentrant locks also support the context management protocol. the `with` statement automatically acquires and releases the lock. |

### 4.2 Context management protocol

```python
with some_lock:
    # do something...
```

is equivalent to:

```python
some_lock.acquire()
try:
    # do something...
finally:
    some_lock.release()
```

### 4.3 Case of Lock & RLock

**Case of Lock**
```python
from time import sleep
from threading import Thread, Lock

class Account(object):
    def __init__(self):
        self._balance = 0
        self._lock = Lock()

    def deposit(self, money):
        # Only acquires the lock can run the below code
        self._lock.acquire()
        try:
            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
        finally:
            # Ensure that locks are properly released
            self._lock.release()
            # pass

    @property
    def balance(self):
        return self._balance
    
account = Account()
print(f'【Start】Balance is {account.balance}')
# create 100 thread execute deposit() at a time
threads = [ Thread(target=account.deposit , args=(1,), name = f'Thread_{i + 1}') for i in range(100) ]
# start and wait complete
for thread in threads: thread.start()
for thread in threads: thread.join()
print(f'【Stop】Balance is {account.balance}')
```

**Case of RLock**
`calculate_total` and `checkout` methods both need to acquire the lock multiple times within a single operation[](在一个操作中多次获取锁) to manipulate[](操作) the `items` attribute. 
If were used `Lock` , this could lead to a deadlock[](死锁). 
However, since we are using `RLock`, these methods can function properly.

```python
import threading

class item:
    def __init__(self):
        self._name = name
        self._price = price
    
class ShoppingCart:
    def __init__(self):
        self.items = []
        self._lock = threading.RLock()

    def add_item(self, item):
        with self._lock:
            self.items.append(item)

    def remove_item(self, item):
        with self._lock:
            self.items.remove(item)

    def calculate_total(self):
        total = 0
        with self._lock:
            for item in self.items:
                # Lock is required here to ensure no item is added or removed during price calculation
                total += item.price
        return total

    def checkout(self):
        with self._lock:
            total = self.calculate_total()
            if total > 0:
                self.process_payment(total)
                self.items.clear()
```

## 5 Condition Objects

### 5.1 Condition Description

The `threading.Condition` object (condition variable) is used to coordinate operations[](协调操作) between threads. It allows one or more threads to wait until a certain condition is met[](满足某个条件) before proceeding[](继续) to the next operation.

| No. | Structure                | type        | Desciption                                                                                       |
| --- | ------------------------ | ----------- | ------------------------------------------------------------------------------------------------ |
| 1   | `Condition(_lock=None_)` | Constructor | used lock as the underlying lock[](底层锁). if it is not given, use a new RLock as underlying lock. |
| 2   | `acquire()`              | func        | Acquire the underlying lock,                                                                     |
| 3   | `release()`              | func        | Release the underlying lock                                                                      |
| 4   | `with _rlock:`           | use way     | `with` statement automatically acquires and releases the underlying lock                         |
| 5   | `wait(timeout=None)`     | func        | Wait until notified or until a timeout occurs.                                                   |
| 6   | `notify_all()`           | func        | Wake up all threads waiting on this condition.                                                   |

### 5.2 Case of Condition

```python
import threading

# This is a shared resource
items = []
condition = threading.Condition()

class Producer(threading.Thread):
    def run(self):
        global items
        while True:
            with condition:
                if len(items) == 0:
                    print("Producer: Adding item.")
                    items.append(1)
                    print("Producer: Notifying consumer.")
                    condition.notify_all()

class Consumer(threading.Thread):
    def run(self):
        global items
        while True:
            with condition:
                if len(items) == 0:
                    print("Consumer: Waiting for item.")
                    condition.wait()
                print("Consumer: Consuming item.")
                items.pop()

Producer().start()
Consumer().start()
```

## 6 Semaphore Objects

### 6.1 Semaphore Description

**threading.Semaphore Description**
* The `threading.Semaphore` object is a synchronization primitive[](同步原语) used to control the number of threads that can simultaneously[](同时地) access a specific resource or perform a specific operation.
* The semaphore maintains an internal counter. If the counter is greater than 0, the `acquire()` call will decrement the counter[](减少计数器) and return immediately[](立刻返回). If the counter is 0, the `acquire()` call will block until another thread calls `release()`.
    * synchronization primitive：The techniques or mechanisms[](技术或机制) used to control the interaction between multiple threads or processes in concurrent programming

**threading.BoundedSemaphore Description** 

* `threading.BoundedSemaphore` is a variant[](变种)of `Semaphore`.
* If a `release()` call attempts to increase the counter's value beyond its initial value[](超过初始化数量), `BoundedSemaphore` will raise a `ValueError` exception. This serves as an error-checking mechanism to prevent incorrect `release` calls.

| No. | Structure                     | type        | Desciption                                                                                                                                                                                                      |
| --- | ----------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Semaphore(_value=1_)`        | Constructor | control the number of threads that can simultaneously[](同时地) access a specific resource or perform a specific operation                                                                                         |
| 2   | `BoundedSemaphore(_value=1_)` | Constructor | control the number of threads that can simultaneously[](同时地) access a specific resource or perform a specific operation, <br>if counter's value attempt beyond its initial value, raise `valueError` exeception |
| 3   | `acquire()`                   | func        | decrement the counter's value, reduce the number of threads                                                                                                                                                     |
| 4   | `release()`                   | func        | increase the counter's value, add threads                                                                                                                                                                       |

### 6.2 BoundedSemaphore And Semaphore

```python
import threading

# Create a bounded semaphore with an initial value of 2
sem = threading.BoundedSemaphore(2)
# sem = threading.Semaphore(2)

# Acquire the semaphore twice
sem.acquire()
sem.acquire()

# This will raise a ValueError, because the semaphore value cannot exceed its initial value
sem.release()
sem.release()
sem.release()
```

### 6.3 Case of BoundedSemaphore

```python
"""
Example of an online movie ticket booking system, assuming there are 10 seats available for reservation(预定)
"""
import threading
import random
import time

class MovieGoer(threading.Thread):
    def __init__(self, sem, name):
        super().__init__()
        self.sem = sem
        self.name = name

    def run(self):
        time.sleep(random.randint(1, 10))  # Simulate time required to make a decision
        print(f"{self.name} is trying to book a seat...")
        self.sem.acquire()  # Try to book a seat
        print(f"{self.name} has booked a seat!")
        time.sleep(random.randint(5, 10))  # Simulate time enjoying the movie
        print(f"{self.name} has left, freeing up their seat.")
        self.sem.release()  # Release the seat

sem = threading.Semaphore(10)  # 10 seats in total

# Create a bunch of movie-goers
moviegoers = [MovieGoer(sem, f"MovieGoer-{i}") for i in range(1, 21)]

for moviegoer in moviegoers:
    moviegoer.start()

```


## 7 Event Objects


### 7.1 threading.Event Description
  
The `Event` object is a simple thread synchronization tool primarily used to trigger events between multiple threads. It contains an internal flag that can be set to true or false using `set()` or `clear()`. If the internal flag of the `Event` object is true, threads calling `wait()` will not be blocked. If the internal flag is false, threads calling `wait()` will be blocked until another thread calls `set()` to set the internal flag to true.

| No. | Structure            | type        | Desciption                                                                                                                                                                                                                                                                                              |
| --- | -------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Event()`            | Constructor |                                                                                                                                                                                                                                                                                                         |
| 2   | `is_set()`           | func        | Return the internal flag, True or False                                                                                                                                                                                                                                                                 |
| 3   | `set()`              | func        | Set the internal flag to true                                                                                                                                                                                                                                                                           |
| 4   | `clear()`            | func        | Set the internal flag to false                                                                                                                                                                                                                                                                          |
| 5   | `wait(timeout=None)` | func        | Block as long as[](只要) the internal flag is false **and** the timeout, if given, has not expired.<br>If no `timeout` are provided, it will wait until the internal flag becomes true. <br>If `timeout` is given, it will wait until the internal flag becomes true **or** the timeout duration expires. |


### 7.2 Case of Event

Suppose[](假设) we are developing a multithreaded network application where one thread is responsible for receiving data from the server, while other threads are used to process this data.
When the receiving thread gets new data, it can use the `Event` object to notify[](通知) the other threads that the data is ready and can be processed.

```python
import threading
import time
import random

def data_receiver(event):
    while True:
        # Simulate delay for receiving data
        time.sleep(random.randint(2, 5)) 
        print("DataReceiver: Received data from the server")
        # Signal that data is ready, internal flag is Ture
        event.set()

def data_processor(event):
    while True:
        print("DataProcessor: Waiting for data...")
        # Wait for data to be ready, wait internal flag to be tr
        event.wait() 
        print("DataProcessor: Processing data...")
        # Reset the event
        event.clear()

event = threading.Event()
receiver = threading.Thread(target=data_receiver, args=(event,))
processor = threading.Thread(target=data_processor, args=(event,))

receiver.start()
processor.start()
```

## 8 Timer Objects

### 8.1 Timer Description

* `threading.Timer` is a subclass of `Thread` and as such also functions as an example of creating custom threads
* `Timer` represents an action that runs for the first time after a specified amount of time. You can think of it as a delayed execution thread[](延迟执行线程).

| No. | Structure                                    | type        | Desciption                                                                                                                      |
| --- | -------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Timer(_interval_, _function_, _args=None_)` | Constructor | `interval` : total delay num, second(s)<br>`function` : thread run logic<br>`arg` : function arg                                |
| 2   | `start()`                                    | func        | Timer started as with threads, after interval second(s), execute function                                                       |
| 3   | `cancel()`                                   | func        | Stop the timer, and cancel the execution of the timer’s action. This will only work if the timer is still in its waiting stage. |

### 8.2 Case of Timer

```python
from threading import Timer

def hello():
    print("hello, world")

t = Timer(3.0, hello)
t.start()  # after 30 seconds, "hello, world" will be printed
```

## 9 Barrier Objects

New in version 3.2.

### 9.1 Barrier Description

* Used to make a group of threads wait on a `threading.Barrier` object. 
* This is a synchronization mechanism for scenarios involving a fixed number of threads that need to wait for each other until all threads are ready to continue execution.

| No. | Structure                                           | type        | Desciption                                                                                                                                                                                                                                                                                                                                        |
| --- | --------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `Barrier(_parties_, _action=None_, _timeout=None_)` | Constructor | `_parties_` : number of threads that need to wait for each other<br>`_action` : an optional callable object that is invoked when all threads have reached the barrier<br>`_timeout` : The default timeout value that will be used for all subsequent[](后续的) `wait()` calls                                                                        |
| 2   | `int wait(_timeout=None_)`                          | func        | `use`：use to wait Barrier.When all threads party of Barrier call `wait()`, they will all be unblocked.If `timeout` is provided, the thread will be unblocked after the specified time, regardless of whether[](不管是否) the other threads have reached the barrier.<br>`return` : integer in the range 0 to _parties_ – 1, different for each thread |
| 3   | `reset()`                                           | func        | Return the barrier to the default, empty state.                                                                                                                                                                                                                                                                                                   |
| 4   | `parties`                                           | Attr        | The number of threads required to pass the barrier                                                                                                                                                                                                                                                                                                |
| 5   | `n_waiting`                                         | Attr        | The number of threads currently waiting in the barrier                                                                                                                                                                                                                                                                                            |

```python
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
```

### 9.2 Case of Barrier
  
Suppose we are developing a multithreaded game application where the game consists of multiple rounds, and each round requires all players to make their decisions before the next round can begin.

The `Barrier` object can be used to ensure that all players are ready to start the next round.

```python
"""
In this example, we create three players, and each player waits for the others after making their decision. Once all players have made their decisions, they all proceed to the next round.

This pattern is commonly used in situations where multiple threads need to start executing simultaneously, such as in multiplayer synchronized games, parallel computing, and more.
"""
import threading
import time
import random

class Player(threading.Thread):
    def __init__(self, barrier):
        super().__init__()
        self.barrier = barrier

    def run(self):
        # Simulate the time needed for a player to take a decision
        time.sleep(random.randint(1, 5))
        print(f"{self.name} is ready for the next round.")
        self.barrier.wait()
        print(f"{self.name} started the next round.")

barrier = threading.Barrier(3)            # waite 

players = [Player(barrier) for _ in range(3)]

for player in players:
    player.start()
```

## 10 Queue

`queue.Queue`  Thread-safe, meaning that when multiple threads operate simultaneously, it will not lead to exceptions (as it internally implements locks).

- **put(item)**：将`item`放入队列。
- **get()**：从队列中移除并返回一个项目。如果队列为空，`get()`会阻塞，直到有项目可用。
- **empty()**：如果队列为空，返回`True`，否则返回`False`。
- **full()**：如果队列已满，返回`True`，否则返回`False`。
- **task_done()**：表示先前的`get()`调用已经处理完一个项目。
- **join()**：阻塞，直到队列中所有的项目都已经被处理。

```python
import time
import threading 

def get_detail_
```

## Else

...