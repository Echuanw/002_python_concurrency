from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import time
"""
Multi Thread exec for : 12.066435813903809
Multi Process exec for : 8.564054250717163
    Multi-CPU operations(e.g., for computations, image processing) :  multiprocessing is better than multithreading
"""
def fib(n):      
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

def main():
    with ThreadPoolExecutor(max_workers = 3) as exec:
        start_time = time.time()
        # all_thread_task = [exec.submit(fn = fib, args = (i,)) for i in range(25, 35)] # TypeError: ThreadPoolExecutor.submit() missing 1 required positional argument: 'fn'
        all_thread_task = [exec.submit(fib, i) for i in range(25, 40)]
        for future in as_completed(all_thread_task):
            print(f"exec thread result is : {future.result()}")
        print(f"Multi Thread exec for : {time.time() - start_time} ")

    with ProcessPoolExecutor(max_workers = 3) as exec:
        start_time = time.time()
        all_process_task = [exec.submit(fib, i) for i in range(25, 40)]
        for future in as_completed(all_process_task):
            print(f"exec process result is : {future.result()}")
        print(f"Multi Process exec for : {time.time() - start_time} ")

if __name__ == '__main__':
    main()
