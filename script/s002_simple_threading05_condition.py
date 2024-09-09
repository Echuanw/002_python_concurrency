import threading

# This is a shared resource
items = []
condition = threading.Condition()

class Producer(threading.Thread):
    def run(self):
        global items
        while True:
            with condition:
                if len(items) == 0:
                    print("Producer: Adding item.")
                    items.append(1)
                    print("Producer: Notifying consumer.")
                    condition.notify_all()

class Consumer(threading.Thread):
    def run(self):
        global items
        while True:
            with condition:
                if len(items) == 0:
                    print("Consumer: Waiting for item.")
                    condition.wait()
                print("Consumer: Consuming item.")
                items.pop()

Producer().start()
Consumer().start()