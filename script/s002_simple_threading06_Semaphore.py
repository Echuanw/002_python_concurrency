"""
Example of an online movie ticket booking system, assuming there are 10 seats available for reservation(预定)
"""
import threading
import random
import time

class MovieGoer(threading.Thread):
    def __init__(self, sem, name):
        super().__init__()
        self.sem = sem
        self.name = name

    def run(self):
        time.sleep(random.randint(1, 10))                  # Simulate time required to make a decision
        print(f"{self.name} is trying to book a seat...")
        with self.sem:                                          # Try to book a seat
            print(f"{self.name} has booked a seat!")
            time.sleep(random.randint(5, 10))                  # Simulate time enjoying the movie
            print(f"{self.name} has left, freeing up their seat.")

sem = threading.Semaphore(10)  # 10 seats in total

# Create a bunch of movie-goers
moviegoers = [MovieGoer(sem, f"MovieGoer-{i}") for i in range(1, 21)]

for moviegoer in moviegoers:
    moviegoer.start()