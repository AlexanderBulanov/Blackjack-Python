""" 
File: blackjack_fsm.py
Author: Alexander Bulanov
"""

# Global Imports #
import random
import time
from enum import Enum

# Local Imports #
from . import blackjack_game_logic as bjl
from . import blackjack_game_objects as bjo
#from . import blackjack_game_settings as bjs
from . import blackjack_players as bjp
from . import cut_helper as cut


### Blackjack State Machine ###
class GameState(Enum):
    STARTING = 0
    WAITING = 1
    SHUFFLING = 2
    DEALING = 3
    SCORING = 4
    PLAYER_PLAYING = 5
    DEALER_PLAYING = 6
    CLEANUP = 7


class BlackjackStateMachine:
    def __init__(self, num_of_decks):
        self.state = GameState.STARTING
        self.num_of_decks = num_of_decks
        self.pen = None
        self.shoe = bjo.get_shoe_of_n_decks(self.num_of_decks)
        self.discard = []
        self.dealer = bjp.Player.create_casino_dealer()
        self.wait_timer_duration = 30
        self.current_wait_timer = self.wait_timer_duration # how long WAITING state lasts once at least 1 player joins, default is 30 seconds
        self.waiting_players = [] # list of players waiting either for a hand or shoe to end, to join
        self.joined_players = [bjp.Player.create_new_player_from_template('Alex')] # list of players currently playing a shoe
        self.known_players = [] # list of all players who have played a shoe, now or in the past
        self.active_player = None
        self.dealer_actions = {
            'deal': lambda: self.deal(),
            'stand': lambda: self.stand(),
            'hit': lambda: self.hit()
        }
        self.player_turn_actions = {
            'skip': lambda: self.skip_turn(),
            'bet': lambda: self.bet(),
            'stand': lambda: self.stand(),
            'hit': lambda: self.hit(),
            'double down': lambda: self.double_down(),
            'split': lambda: self.split(),
            'surrender': lambda: self.surrender(),
            'insurance': lambda: self.insurance(),
            'even money': lambda: self.even_money()
        }
        self.player_connection_actions = {
            'join': lambda: self.join(),
            'leave': lambda: self.leave()
        }

    def transition(self, next_state):
        self.state = next_state

    

    # Player Turn Actions #
    def skip_turn(self):
        pass
    
    def bet(self):
        pass
    
    def stand(self):
        self.transition(GameState.DEALING)

    def hit(self):
        pass

    def double_down(self):
        pass

    def split(self):
        pass

    def surrender(self):
        pass

    def insurance(self):
        pass

    def even_money(self):
        pass

    # Player Connection Actions #
    def join(self):
        pass

    def leave(self):
        pass

    """
    def hit(self):
        # Deal 1 card from the deck
        self.hand.extend([self.shoe.pop()])
        print("Player hand after hit is:",self.hand)
        self.transition(GameState.SCORING)
    """

    # Debug #
    def dump_state_machine_data(self):
        print("*  *  *")
        print("START - DUMPING STATE MACHINE DATA")
        for attr, value in self.__dict__.items():
            if attr == 'shoe':
                print('shoe_size:',len(self.shoe))
                print(attr+': '+str(value))
            elif attr == 'discard':
                print('discard_size:',len(self.discard))
                print(attr+': '+str(value))
            else:
                print(attr+': '+str(value))
        print("END OF DUMPING ALL STATE MACHINE DATA")
        print("*  *  *")

    def dump_shoe_data(self):
        print("*  *  *")
        print("START - DUMPING SHOE DATA")
        print('shoe_size:',len(self.shoe))
        print('discard_size:',len(self.discard))
        for attr, value in self.__dict__.items():
            if attr == 'shoe':
                print(attr+': '+str(value))
            elif attr == 'discard':
                print(attr+': '+str(value))
        print("END OF DUMPING SHOE DATA")
        print("*  *  *")

    def dump_state_mode(self):
        pass
    # Can use diff before/after a function call on generated text files
    # How to toggle this automatically w/o manually adding conditionals before/after?

    def print_missing_cards_in_single_deck_shoe_if_any(self):
        missing_cards = list(set(bjo.base_deck).difference(set(self.shoe)))
        if len(missing_cards) == 0:
            print("*** No cards missing in shoe ***")
        else:
            print("*  *  *")
            print(len(bjo.base_deck), "CARDS IN REFERENCE SINGLE DECK:")
            print(bjo.base_deck)
            print(len(self.shoe), "CARDS IN SHOE:")
            print(self.shoe)
            print("The following cards are missing -", missing_cards)
            print("*  *  *")

    def print_all_hands(self):
        print("*  *  *")
        print(self.dealer.name, "has hand of", self.dealer.current_hands)
        print("  *  *  ")
        for player in self.joined_players:
            print(player.name, "has the following hands:", player.current_hands)



    # State Machine Actions #
    def wait_for_players(self):
        print("Waiting for players to join...")
        while self.current_wait_timer != 0:
            if len(self.waiting_players) == 0:
                # Reset timer if waiting player count drops to zero at any point before timer expires
                self.current_wait_timer = self.wait_timer_duration
            else:
                print("Game starting in",self.current_wait_timer,"seconds, waiting for more players to join...")
                time.sleep(1)
                self.current_wait_timer -= 1
        # Reset timer and transition to next state
        self.current_wait_timer = self.wait_timer_duration
        self.transition(GameState.STARTING)
                
    def start_game(self):
        print("STARTING GAME")
        # Initialize first player (sitting leftmost w.r.t. dealer) to be active
        #self.joined_players[0].is_active = True
        self.active_player = self.joined_players[0]
        # Add all joined players to known
        # YOUR CODE HERE
        self.transition(GameState.SHUFFLING)

    def shuffle_cut_and_burn(self, cut_percentage):
        # Remove both cut cards as necessary
        if 'front_cut_card' in self.discard:
            self.discard.remove('front_cut_card')
            self.shoe.remove('back_cut_card')
            # Put discard pile back into the shoe to shuffle
            self.shoe.extend(self.discard)
            self.discard.clear()
            """
            # DEBUG #
            self.dump_deck_data()
            self.print_missing_cards_in_shoe_if_any()
            """
        # Shuffle
        random.shuffle(self.shoe)
        # Cut (twice)
        cut.first_cut(self.shoe)
        self.pen = cut.second_cut(self.shoe, cut_percentage)
        # Burn (first card in the shoe)
        self.discard.extend([self.shoe.pop(0)])
        print("Burned card is", self.discard)
        self.transition(GameState.DEALING)


    def round_end_handler(self):
        print("ROUND END")
        # Reshuffle at round end if 'front_cut_card' was reached
        if 'front_cut_card' in self.discard:
            print("SHOE END, reshuffling!")
            self.transition(GameState.SHUFFLING)
        else:
            self.transition(GameState.DEALING)


    def score_hand(self):
        self.score = bjl.highest_hand_score(self.hand)
        if (self.score == 21):
            print("Blackjack!")
            self.discard.extend(self.hand)
            self.round_end_handler()
        elif (self.score == -1):
            print("Bust!")
            self.discard.extend(self.hand)
            self.round_end_handler()
        else:
            self.transition(GameState.PLAYING)
        print("Player score is:", self.score)
        return self.score

    def deal(self):
        for x in range(0, 2):
            # Deal a card to each player, then dealer, repeat once
            for player in self.joined_players:
                # Slide 'front_cut_card' to discard if encountered when dealing any In-Round hand
                if ('front_cut_card' == self.shoe[0]):
                    self.discard.extend([self.shoe.pop(0)])
                player.current_hands.extend([self.shoe.pop(0)])
            # Slide 'front_cut_card' to discard if encountered when dealing any In-Round hand
            if ('front_cut_card' == self.shoe[0]):
                self.discard.extend([self.shoe.pop(0)])
            self.dealer.current_hands.extend([self.shoe.pop(0)])
        # Print debug info on players hands and % of shoe dealt
        self.print_all_hands()
        #print("Player hand is: "+str(self.hand))
        print(str(int(round(100-(100*(len(self.shoe)/(2+self.num_of_decks*52))), 0)))+"%"+" of the shoe dealt "
            +"(reshuffling at round end past "+str(self.pen)+"%"+")")
        self.transition(GameState.SCORING)

    def play(self):
        # Get action from currently active player (starting leftmost at hand start)
        self.active_player.action = input("Enter an action: ").strip().lower()
        # Check that active player action is valid
        if self.active_player.action not in self.player_turn_actions:
            print("Unknown action", repr(self.active_player.action), "entered, please enter one of the following: stand")
        else:
            print("Executing Player "+self.active_player.name+"'s action "+repr(self.active_player.action))
            # Execute player's entered action
            if self.active_player.action == 'stand':
                pass


            self.player_turn_actions[self.active_player.action]()


            self.discard.extend(self.hand)
            self.round_end_handler()

    def step(self):
        print(f"Current state: {self.state}")
        match self.state:
            case GameState.WAITING:
                self.wait_for_players()
            case GameState.STARTING:
                self.start_game()
            case GameState.SHUFFLING:
                self.shuffle_cut_and_burn(None) # Todo: AB - pen % is different upon each reshuffle in a single session
            case GameState.DEALING:
                self.deal()
            case GameState.SCORING:
                self.score_hand()
            case GameState.PLAYING:
                self.play()
            case other:
                print("Invalid state!")
                raise NameError

    def run(self):
        self.dealer.print_player_stats()
        self.joined_players[0].print_player_stats()
        try:
            while True:
                self.step()
        except KeyboardInterrupt:
                print("\nExiting state machine...")
                #running = False
                #print("Running has been set to",running)





"""
def add_state(self, prev_state, next_state, transition_condition, transition_output):
    self.state = next_state

def add_transition(self, start_state, end_state):
    # How to store transitions?
    #self.state = end_state
    pass
"""


"""
game = BlackjackSM()
game.run()
"""