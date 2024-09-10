Currently, there is only one module in this package
* `concurrent.futures` – Launching parallel tasks

## 1 concurrent.futures Desciption

The concurrent.futures module provides a high-level interface for asynchronously executing callables[](异步执行可调用对象).
It provides two main components: the `Executor` object and the `Future` object.

- **Executor**：
	- abstract class, two concrete subclasses[](具体子类): 
		- `ThreadPoolExecutor` :  
		- `ProcessPoolExecutor` : 
	- defines methods for managing and scheduling asynchronous tasks
	- Commonly used methods include `submit()`, `map()`, and `shutdown()`.
- **Future**：
	- represents a result of a computation that may not yet be completed, You can think of a `Future` object as a handle for tasks submitted to the `Executor`.
	- provides a way to check the status of a task, retrieve the task's result, or cancel the task.
	- Commonly used methods include `result()`, `done()`, and `cancel()`.

**`concurrent.futures` Module Function**

| No. | Abstract Function                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `wait(fs, timeout=None, return_when=ALL_COMPLETED)` | Accepts an iterable of `Future` instances and blocks until a specified condition is met. The return value is a tuple containing two sets: one for completed `Future` instances and another for uncompleted `Future` instances.<br>specified condition `return_when`:<br>- `ALL_COMPLETED`  when all futures finish or are cancelled<br>- `FIRST_EXCEPTION` when any future raising an exception or `ALL_COMPLETED`<br>- `FIRST_COMPLETED` when any future finishes or is cancelled. |
| 2   | `as_completed(fs, timeout=None)`                    | Accepts an iterable of `Future` instances and returns a new iterator that yields each `Future` as it completes.<br>Means, A group of futures where the result of the first completed future is obtained first. Retrieve futures results based on their completion time.                                                                                                                                                                                                             |



## 2 Executor & Future Objects

### 2.1 Executor 

| No. | Abstract Function                                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | `submit(fn, /, *args, **kwargs)`                 | executed as fn(*args, **kwargs) and returns a Future object immedility                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 2   | `map(fn, *iterables, timeout=None, chunksize=1)` | Similar to map_async(fn, *iterables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| 3   | `shutdown(wait=True, *, cancel_futures=False)`   | wait : Whether to block the calling thread until all unfinished tasks are completed<br>- wait=True, all the pending futures are done and the resources have been freed then method return.<br>- wait=False, method will return immediately and wait all pending futures are done and the resources will freed.<br><br>cancel_futures : Whether to cancel all unstarted Future objects. any futures that are completed or running won’t be cancelled<br>- cancel_futures=False, method will not cancel all pending futures<br>- cancel_futures=True, method will cancel all pending futures |

### 2.2 Future⭐

task 返回容器，task返回结果都会向Future里面放。
如果调用了submit, 他会把task交给内部的 `_WorkItem` 执行，workItem 中，他是先执行task函数，然后将结果 rst 或 err 设置到 Future 对象中间去，最后返回 Future 对象。

| No. | Function                  | Description                                                                                                                                                                                                                                        |
| --- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `cancel()`                | Attempt to cancel the call. <br>If it is currently being executed or finished running and cannot be cancelled then return False, otherwise the call will be cancelled and return True.                                                             |
| 2   | `done()`                  | Return True if the call was successfully cancelled or finished running.                                                                                                                                                                            |
| 3   | `result(timeout=None)`    | Return the value returned by the call. <br>If the call hasn’t completed in timeout seconds, then raise `TimeoutError`<br>If it is cancelled before completing then raise `CancelledError`<br>If it completed without raising, returned call return |
|     | `exception(timeout=None)` | Return the exception raised by the call.<br>If the call hasn’t completed in timeout seconds, then raise `TimeoutError`<br>If it is cancelled before completing then raise `CancelledError`<br>If it completed without raising, returned `None`     |


## 3 ThreadPoolExecutor

`concurrent.futures.ThreadPoolExecutor`

| No. | Function                                                                                     | Description                                                                                                                                                             |
| --- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `ThreadPoolExecutor(max_workers=None, thread_name_prefix='', initializer=None, initargs=())` | `max_workers` : default `os.cpu_count(*) * 5`<br>`thread_name_prefix`<br> `initializer`&`initargs` : init func and its args, it will be called before each thread start |

```python
import concurrent.futures
import time

def task_initializer(): 
	print("Task thread is starting") 

# simulate task 
def long_running_task(seconds):
    print(f'Starting task that will take {seconds} seconds')
    time.sleep(seconds)
    print(f'Finished task that took {seconds} seconds')
    return seconds

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(
	    max_workers = 4,
	    thread_name_prefix = 'TaskThreadPool',
	    initializer=task_initializer
	    ) as executor:
	    
        # use submit task ,it will return a future obj
        future = executor.submit(long_running_task, 3)
        # use result() to get call back
        result = future.result()
        print(f"The task returned: {result}")

        # submit multi task and get result
        futures = [executor.submit(long_running_task, i) for i in range(2, 5)]
        # list is ordered, and while iterating through it sequentially, some tasks may be running and not yet completed. 
        # Therefore, using `as_completed()` to obtain an iterator allows you to retrieve `Future` objects based on their completion time.
        for future in concurrent.futures.as_completed(futures):
            print(f'Task returned: {future.result()}')
```

## 4 ProcessPoolExecutor

`concurrent.futures.ProcessPoolExecutor`

| No. | Function                                                                                                          | Description                                                                                                                                                                                                                                              |
| --- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `ProcessPoolExecutor(max_workers=None, mp_context=None, initializer=None, initargs=(), max_tasks_per_child=None)` | `max_workers` : default `os.cpu_count(*)`<br>`mp_context` : allow users to control the start_method for worker processes created by the pool<br>`initializer`&`initargs` : init func and its args, it will be called at the start of each worker process |

```python
import concurrent.futures

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(n**0.5) + 1
    for i in range(3, sqrt_n, 2):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    numbers = [i for i in range(10**12, 10**12 + 200)]
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(numbers, executor.map(is_prime, numbers)):
            print('%d is prime: %s' % (number, prime))
```

