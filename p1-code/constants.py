from enum import Enum
from dataclasses import dataclass
import os

class Suit(Enum):
    SPADES = 4
    HEARTS = 3
    DIAMONDS = 2
    CLUBS = 1

@dataclass
class ExchangeState:
    exchange_chance = True
    exchange_round = 0
    exchange_player = -1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')