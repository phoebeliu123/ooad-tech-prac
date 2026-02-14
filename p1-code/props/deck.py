from .card import Card
from constants import Suit
import random

class Deck:
    def __init__(self):
        self.cards_list = []
        self.initial_deck()

    def print_deck(self):
        print(self.cards_list)
        return

    def initial_deck(self):
        for suit in Suit:
            for rank in range(2, 15):
                new_card = Card(suit, rank)
                self.cards_list.append(new_card)
        return
    
    def shuffle(self):
        random.shuffle(self.cards_list)
        return

    def draw(self):
        if self.cards_list:
            new_card = self.cards_list.pop(0)
            return new_card
        else:
            print("deck has no card left")
            return