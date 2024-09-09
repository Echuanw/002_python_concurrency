

所有进程的调度都依靠操作系统的支持。你使用哪种操作系统，Python 会提供对应操作系统的 Python 虚拟机，来大同与操作系统底层相关的服务通道来实现。

  > https://docs.python.org/3/library/multiprocessing.html

## 1 Create Process

Two basic way to create
* Create object by  `Process` Class in `multiprocessing` module 
* Create object by Class which inherting from `Process` Class

### 1.1 Create Process object

```python
from multiprocessing import Process, current_process 
import time

""" 
    The First use script of Process : s001_simple_multiprocessing01.py
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


### 1.2 Create Custom Process object

```python
from multiprocessing import Process, current_process 
import time

""" 
    The Second use script of Process : s001_simple_multiprocessing02.py
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

## 2 Process Control

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

## 3 Daemon

在进程执行过程之中，如果某一个进程启动了，那么一般都是执行到完，但是也可以由另外的一个进程来进行结束的处理。
在一个 Python 应用过程之中，每一个进程启动都意味着要配置其处理的业务逻辑(业务子进程)，但是某些进程在执行的时候可能需要其他进程的帮助。例如:富豪的生活里面是需要有仆人的，仆人为其穿衣服，，为其喂饭，为其拿手机。
在操作系统里面，也可以针对于某一个进程来设置一些辅助的进程，而这样的进程就称为守护进程。



假设现在要做一个数据聊天的功能，但是需要将每一次的聊天记录进行存档，因此可以编写一个守护进程，把每次发送的数据异步上传到服务器上，从而实现员工的监控。

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

## 线程池

   > https://docs.python.org/3/library/concurrent.futures.html
   
`concurrent.futures` module provides a high-level interface for asynchronously executing callables.

所谓的“XX 池”，都属于对资源的统一管理。
如果一个操作系统之中无限制的增加进程，就一定会影响到其他进程的执行速度。
因此为了可以保证进程处于一个服务端硬件环境合理的范围之中，就需要有效的控制进程数量，通过进程池来实现。
进程池中的进程梳理，一般都建议与CPU的内核数量相同。



```python

```