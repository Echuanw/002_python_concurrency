import threading

# Create a bounded semaphore with an initial value of 2
# sem = threading.BoundedSemaphore(2)
sem = threading.Semaphore(2)

# Acquire the semaphore twice
sem.acquire()
sem.acquire()

# ValueError: Semaphore released too many time
sem.release()
sem.release()
sem.release()