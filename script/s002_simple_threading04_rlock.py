from time import sleep
from threading import Thread, Lock

import threading
import random
"""
`calculate_total` and `checkout` methods both need to acquire the lock multiple times within a single operation[](在一个操作中多次获取锁) to manipulate[](操作) the `items` attribute. 
If were used `Lock` , this could lead to a deadlock[](死锁). 
However, since we are using `RLock`, these methods can function properly.
"""
class item:
    def __init__(self, name, price):
        self._name = name
        self._price = price
    
    @property
    def price(self):
        return self._price

class ShoppingCart:
    def __init__(self):
        self.items = []
        self._lock = threading.RLock()

    def add_item(self, item):
        with self._lock:
            self.items.append(item)

    def remove_item(self, item):
        with self._lock:
            self.items.remove(item)

    def calculate_total(self):
        total = 0
        with self._lock:
            for item in self.items:
                # Lock is required here to ensure no item is added or removed during price calculation
                total += item.price
        return total

    def process_payment(self, total):
        pass

    def checkout(self):
        with self._lock:
            total = self.calculate_total()
            if total > 0:
                self.process_payment(total)
                self.items.clear()
    

shopcart = ShoppingCart()

def random_process(shopcart, opt):
    match random.randint(1,9):
        case 1 | 2 | 3 | 4 | 5 | 6:
            shopcart.add_item(item(f"item_{opt}", opt))
            print(f"{threading.current_thread().name} add {opt}")
        case 7 | 8 :
            print(f"【Total】{threading.current_thread().name} check total price is {shopcart.calculate_total()}")
        case 9:
            shopcart.checkout()
            print(f"【clean】{threading.current_thread().name} clean")
        case _:
            print("default case")

threads = [ Thread(target=random_process, args=(shopcart,i, ), name = f'Thread_{i+1}') for i in range(20) ]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()