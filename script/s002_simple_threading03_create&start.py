from threading import Thread, current_thread
import time

""" 
    The First use script of Thread 
    1 Thread Attribute : native_id, name, daemon
    2 Create Thread object by Thread Contributor
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
