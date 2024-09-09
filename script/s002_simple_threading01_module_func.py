"""
Use case of module function
"""
import threading 
def worker(): 
    if threading.current_thread() == threading.main_thread():
        print("【On main thread】")
    else:
        print("【Not on main thread】")
    print(f"Worker thread is: {threading.current_thread().name}")             # MainThread  |  Thread-1 (worker)
    print(f"Active threads: {threading.active_count()}")                      # 1           |  2
    print(f"Worker thread id: {threading.get_ident()}")

# main
worker()
print("#################################################################")
# new thread
thread= threading.Thread(target=worker) 
thread.start()