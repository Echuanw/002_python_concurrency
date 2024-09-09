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
