from multiprocessing import Process, current_process 
import time

""" 
    The Third use script of Process : s002_simple_multiprocessing03.py
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
