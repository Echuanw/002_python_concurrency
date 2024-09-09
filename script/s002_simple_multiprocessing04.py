from multiprocessing import Process, current_process 
import time

""" 
    The fifth use script of Process : s002_simple_multiprocessing04.py
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
