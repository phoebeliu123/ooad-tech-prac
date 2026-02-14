from constants import Suit

class Card:
    def __init__(self, suit: Suit, rank: int):
        self.rank = rank
        self.suit = suit
    
    def __repr__(self):
        rank_map = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
        display_rank = rank_map.get(self.rank, self.rank)
        return f"[{self.suit.name} {display_rank}]"