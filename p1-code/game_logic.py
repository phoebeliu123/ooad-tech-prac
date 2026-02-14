from players import AI, Human
from props import Deck, Card
from constants import ExchangeState, clear_screen
import random


class PockerGame:
    def __init__(self):
        random.seed(100)
        self.player_list = [Human(), Human(), AI(), AI()]
        self.ply_exchange_state = [ExchangeState(), ExchangeState(), ExchangeState(), ExchangeState()]
        self.game_deck = Deck()
    
    def start_game(self):
        print("[Host] Pocker Game Start!")

        # 1.1: Players name themself
        for i , player in enumerate(self.player_list):
            print(f"[Host] Hello! Player{i+1}")
            player.choose_name()
            clear_screen()
            if i < 3:
                print(f"[Host] Pass the turn to Player{i+2}.")
            else:
                clear_screen()
        
        print(f"[Host] Welcome {self.player_list[0].name}, {self.player_list[1].name}, {self.player_list[2].name}, {self.player_list[3].name} join the game!")

        # 1.2: shuffle the deck
        print(f"[Host] Start shuffling the deck.")
        self.game_deck.shuffle()

        # 1.3: deal cards for players
        print(f"[Host] Start dealing cards!")
        for i in range(13):
            for player in self.player_list:
                print(f"[Host] It's Player {player.name}'s turn. Please take the controls.")
                input(f"if Player {player.name} ready to check the result, please click enter.")
                player.gain_hands(self.game_deck)
                if isinstance(player, Human):
                    print(f"[Host] Your hands consists of:")
                    player.print_hands()
                    input("[Host] click enter if you ready to pass the turn to next player.")
                clear_screen()

        # main loop for game
        while any(player.hands for player in self.player_list):
            '''
            遊戲規則補充:
            1. 若玩家還有手牌就有資格參與下一輪的競技，直到手牌用完為止。
            2. 交換手牌的對象只可以挑選沒有在進行交換、持有原本手牌的玩家。
            '''
            # 1.4: determine who can join the next round game.
            rnd_ply_idx = self.det_rnd_ply()
            for idx in rnd_ply_idx:
                print(f"Player {self.player_list[idx].name} join this round.")
            
            rnd_res_map: dict[int, Card] = {}
            for idx in rnd_ply_idx:
                print(f"[Host] It's Player{idx+1} ({self.player_list[idx].name})'s turn. Please take the controls.")
                input(f"[Host] if Player{idx+1} ({self.player_list[idx].name}) ready to check the result, please click enter.")
                clear_screen()
                print(f"[Host] Player{idx+1} ({self.player_list[idx].name}) -- here is your hand cards:")
                print(self.player_list[idx].hands)

                # 1.5: Check the exchcange qualified of Player
                if self.ply_exchange_state[idx].exchange_chance:
                    if self.ply_exchange_state[idx].exchange_round == 0:
                        # 1.5.1: Ask for willing to exchange with others.
                        print("[Host] Do you want to exchange hands with other players.")
                        reply = self.player_list[idx].will_to_exchange()
                        if reply == "y":
                            # 1.5.2: Check the player list for the players who are able to exchange hand cards.
                            exchng_ply_idx = self.can_exchng_ply(idx)
                            if exchng_ply_idx:
                                # 1.6: Start Exchanging
                                print("[Host] Below list is the players who can exchange with you")
                                for i in exchng_ply_idx:
                                    print(f"Index{i}: Player{i+1} ({self.player_list[i].name})")
                                ans = None
                                while True:
                                    ans = input("[Host] Please enter the idx of the player who you want to exchange: ").strip()
                                    if ans.isdigit() and int(ans) in exchng_ply_idx:
                                        ans = int(ans)
                                        break
                                    print("Invalid input! Please enter a valid index from the list.") 
                                ans = int(ans)
                                self.player_list[idx].exchange(self.player_list[ans])
                                self.ply_exchange_state[idx].exchange_chance = False
                                self.ply_exchange_state[idx].exchange_round = 1
                                self.ply_exchange_state[idx].exchange_player = ans
                                self.ply_exchange_state[ans].exchange_round = 1
                                print("[Host] Finish exchanging.")
                                print(f"[Host] Player{idx+1} ({self.player_list[idx].name}) here is your new hand cards:")
                                print(self.player_list[idx].hands)
                                input(f"[Host] Click enter if you finished checking your hand cards. Pass the control to Player{ans+1} ({self.player_list[ans].name})")
                                clear_screen()
                                # skip for ai player
                                if isinstance(self.player_list[ans], Human):
                                    print(f"[Host] Hello, Player{ans+1} ({self.player_list[ans].name}), your hand cards have been changed.")
                                    input("Here is your new hand cards: (click enter to see.)")
                                    print(self.player_list[ans].hands)
                                    input(f"[Host] Click enter if you finished checking your hand cards. Pass the control to Player{idx+1} ({self.player_list[idx].name})")
                                    clear_screen()
                                else:
                                    input(f"Player{ans+1} ({self.player_list[ans].name}) is ai, enter to skip.")
                                    clear_screen()
                                input(f"[Host] Player{idx+1} ({self.player_list[idx].name}) -- here is your hand cards:")
                                print(self.player_list[idx].hands)
                            else:
                                print("No one is ready to exchange with you now, please wait till next round.")
                        else:
                            pass
                else:
                    # if exchange_player != -1 means the player is the one who initiate a card exchange.
                    if self.ply_exchange_state[idx].exchange_player != -1:
                        # if exchange_round = 3 means it has already pass 3 rounds after exchange
                        if self.ply_exchange_state[idx].exchange_round > 3:
                            obj_idx = self.ply_exchange_state[idx].exchange_player
                            print(f"[Host] Time for return the hand cards to Player{obj_idx+1} ({self.player_list[obj_idx].name})")
                            self.player_list[idx].exchange(self.player_list[obj_idx])
                            self.ply_exchange_state[idx].exchange_round = 0
                            self.ply_exchange_state[idx].exchange_player = -1
                            self.ply_exchange_state[obj_idx].exchange_round = 0
                            print("[Host] Finish exchanging.")
                            print(f"[Host] Player{idx+1} ({self.player_list[idx].name}) here is your new hand cards:")
                            print(self.player_list[idx].hands)
                            input(f"[Host] Click enter if you finished checking your hand cards. Pass the control to Player{obj_idx+1} ({self.player_list[obj_idx].name})")
                            clear_screen()
                            if isinstance(self.player_list[obj_idx], Human):
                                print(f"[Host] Hello, Player{obj_idx+1} ({self.player_list[obj_idx].name}), your hand cards have been changed, here is your new hand cards:")
                                print(self.player_list[obj_idx].hands)
                                input(f"[Host] Click enter if you finished checking your hand cards. Pass the control to Player{idx+1} ({self.player_list[idx].name})")
                                clear_screen()
                            else:
                                input(f"Player{obj_idx+1} ({self.player_list[obj_idx].name}) is ai, enter to skip.")
                                clear_screen()
                            print(f"[Host] Player{idx+1} ({self.player_list[idx].name}) -- here is your hand cards:")
                            print(self.player_list[idx].hands)

                # 1.7: make the decision
                if self.player_list[idx].hands:
                    rnd_res_map[idx] = self.player_list[idx].decision()
                clear_screen()

            # 1.8: display the showing cards
            for key, card in rnd_res_map.items():
                print(f"[Host] Player{key+1} ({self.player_list[key].name}) shows {card}")
            
            # 1.9: compare the result
            if rnd_res_map:
                winner_id = self.comparing(rnd_res_map)
                print(f"[Host] The round winner is Player{winner_id+1} ({self.player_list[winner_id].name})")
                # 1.10: winner get 1 point
                self.player_list[winner_id].add_point()
            else:
                print("[Host] This round no one showing the card.")
            
            for state in self.ply_exchange_state:
                if state.exchange_round > 0:
                    state.exchange_round = state.exchange_round + 1
            input()
            clear_screen()
        
        # 1.11: show the final winner
        print(f"[Host] The Game has ended.")
        print(f"--- score board ---")
        for i, player in enumerate(self.player_list):
            print(f"Player{i+1} ({player.name}) --- {player.point}")
        win_ids = self.show_winner()

        for i in win_ids:
            print(f"[Host] The final winner is Player{i+1} ({self.player_list[i].name})!")
        
        print("[Host] Game Over!!!")

        

    def show_winner(self):
        max_point = max(p.point for p in self.player_list)
        winners = [i for i, p in enumerate(self.player_list) if p.point == max_point]
        return winners

    def comparing(self, rnd_res_map):
        winner_id = None
        best_card = None

        for player_id, current_card in rnd_res_map.items():
            if winner_id is None:
                winner_id = player_id
                best_card = current_card
                continue
            
            if current_card.rank > best_card.rank:
                winner_id = player_id
                best_card = current_card
                
            elif current_card.rank == best_card.rank:
                if current_card.suit.value > best_card.suit.value:
                    winner_id = player_id
                    best_card = current_card
        return winner_id
    
    def det_rnd_ply(self):
        rnd_ply_idx = []
        for i, player in enumerate(self.player_list):
            if player.hands:
                rnd_ply_idx.append(i)
        return rnd_ply_idx

    def can_exchng_ply(self, my_idx):
        ply_idx = []
        for i, player in enumerate(self.ply_exchange_state):
            if player.exchange_round == 0:
                ply_idx.append(i)
        ply_idx.remove(my_idx)
        return ply_idx
