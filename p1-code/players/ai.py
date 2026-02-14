import random
from .player_base import Player

class AI(Player):
    def __init__(self):
        super().__init__()

    def choose_name(self):
        name = "ai-" + str(random.randint(1000, 9999))
        self.name = name

    def will_to_exchange(self):
        choice = "n"
        return choice

    def decision(self):
        if not self.hands:
            print("you don't have any hand card left.")
            return
        random_idx = random.randrange(len(self.hands))    
        return self.hands.pop(random_idx)