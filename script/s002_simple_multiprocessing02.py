from multiprocessing import Process, current_process 
import time

""" 
    The Second use script of Process : s002_simple_multiprocessing02.py
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
    # for p in process_arr:
    #     p.join()

if __name__ == '__main__':
    main()
