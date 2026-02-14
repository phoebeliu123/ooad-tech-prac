from __future__ import annotations
from props import Card, Deck

class Player:
    def __init__(self):
        self.__name: str | None = None
        self.__point: int = 0
        self.hands: list[Card] = []
    
    @property
    def name(self):
        return self.__name or "No name"
    
    @name.setter
    def name(self, name: str | None = None):
        print("setting name")
        self.__name = name
    
    @property
    def point(self):
        return self.__point
    
    @point.setter
    def point(self, pt):
        self.__point = pt

    def gain_hands(self, deck: Deck = None):
        new_card = deck.draw()
        self.hands.append(new_card)

    def print_hands(self):
        print(self.hands)
    
    def decision(self):
        pass

    def choose_name(self):
        pass
    
    def add_point(self):
        self.__point = self.__point + 1
    
    def will_to_exchange(self):
        pass
    
    def exchange(self, player: Player):
        self.hands, player.hands = player.hands, self.hands 
    
        


