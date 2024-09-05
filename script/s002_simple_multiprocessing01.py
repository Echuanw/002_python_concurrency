from multiprocessing import Process, current_process 
import time

""" 
    The First use script of Process : s002_simple_multiprocessing01.py
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
