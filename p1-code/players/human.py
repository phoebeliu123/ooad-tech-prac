from .player_base import Player

class Human(Player):
    def __init__(self):
        super().__init__()

    def choose_name(self):
            while True:
                name = input("Please enter your name: ").strip()
                if name:
                    self.name = name
                    break
                print("Name cannot be empty! Please try again.")

    def will_to_exchange(self):
        while True:
            choice = input("Do you want to exchange? (y for yes, n for no): ").strip().lower()
            if choice in ['y', 'n']:
                return choice
            print("Invalid input! Please enter 'y' or 'n'.")

    def decision(self):
        if not self.hands:
            print("You have no cards to play!")
            return None

        print("\n--- Your current hand cards ---")
        for i, card in enumerate(self.hands):
            print(f"Index: {i}, Card: {card}")
        
        while True:
            idx_str = input(f"Please enter the index (0-{len(self.hands)-1}) of the card you want to show: ").strip()

            if not idx_str.isdigit():
                print("Error: Please enter a valid positive number.")
                continue
            idx = int(idx_str)
            if 0 <= idx < len(self.hands):
                return self.hands.pop(idx)
            else:
                print(f"Error: Index out of range. Please choose between 0 and {len(self.hands)-1}.")