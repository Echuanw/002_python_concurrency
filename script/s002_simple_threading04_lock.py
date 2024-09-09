from time import sleep
from threading import Thread, Lock

class Account(object):
    def __init__(self):
        self._balance = 0
        self._lock = Lock()

    def deposit(self, money):
        # Only acquires the lock can run the below code
        self._lock.acquire()
        try:
            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
        finally:
            # Ensure that locks are properly released
            self._lock.release()
            # pass

    @property
    def balance(self):
        return self._balance
    
account = Account()
print(f'【Start】Balance is {account.balance}')
# create 100 thread execute deposit() at a time
threads = [ Thread(target=account.deposit , args=(1,), name = f'Thread_{i + 1}') for i in range(100) ]
# start and wait complete
for thread in threads: thread.start()
for thread in threads: thread.join()
print(f'【Stop】Balance is {account.balance}')