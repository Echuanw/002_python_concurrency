"""
In this example, we create three players, and each player waits for the others after making their decision. Once all players have made their decisions, they all proceed to the next round.

This pattern is commonly used in situations where multiple threads need to start executing simultaneously, such as in multiplayer synchronized games, parallel computing, and more.
"""
import threading
import time
import random

class Player(threading.Thread):
    def __init__(self, barrier):
        super().__init__()
        self.barrier = barrier

    def run(self):
        # Simulate the time needed for a player to take a decision
        time.sleep(random.randint(1, 5))
        print(f"{self.name} is ready for the next round.")
        self.barrier.wait()
        print(f"{self.name} started the next round.")

barrier = threading.Barrier(3)            # waite 

players = [Player(barrier) for _ in range(3)]

for player in players:
    player.start()