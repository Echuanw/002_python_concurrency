from multiprocessing import Process, Manager 
import time

""" 
    Manager().dict() can share between processes. If in multiprocess , you should use Synchronization primitives(RLock, condition ...) to ensure process safety.
"""

def add_data(p_dict, key, value):
    p_dict[key] = value

def main():
    process_dict = Manager().dict()

    p_1 = Process(target=add_data, args=(process_dict, 'p_1', 11))
    p_2 = Process(target=add_data, args=(process_dict, 'p_2', 12))
    p_1.start()
    p_2.start()
    p_1.join()
    p_2.join()
    # first , update process_dict in each process
    # secound, print process_dict in main process
    print(process_dict)   # {'p_1': 11, 'p_2': 12}

if __name__ == '__main__':
    main()
