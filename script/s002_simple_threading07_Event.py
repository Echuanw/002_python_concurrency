import threading
import time
import random

def data_receiver(event):
    while True:
        # Simulate delay for receiving data
        time.sleep(random.randint(2, 5)) 
        print("DataReceiver: Received data from the server")
        # Signal that data is ready, internal flag is Ture
        event.set()

def data_processor(event):
    while True:
        print("DataProcessor: Waiting for data...")
        # Wait for data to be ready, wait internal flag to be tr
        event.wait() 
        print("DataProcessor: Processing data...")
        # Reset the event
        event.clear()

event = threading.Event()
receiver = threading.Thread(target=data_receiver, args=(event,))
processor = threading.Thread(target=data_processor, args=(event,))

receiver.start()
processor.start()