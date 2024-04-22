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
from . import blackjack_players as bjp
from . import cut_helper as cut


### Blackjack State Machine ###
class GameState(Enum):
    STARTING = 0
    SHUFFLING = 1
    DEALING = 2
    SCORING = 3
    PLAYER_PLAYING = 4
    DEALER_PLAYING = 5
    ROUND_ENDING = 6


class BlackjackStateMachine:
    def __init__(self, num_of_decks):
        self.state = GameState.STARTING
        self.num_of_decks = num_of_decks
        self.pen = None
        self.shoe = bjo.get_shoe_of_n_decks(self.num_of_decks)
        self.discard = []
        self.dealer = bjp.Player.create_casino_dealer()
        self.seventeen_rule = 'S17'
        self.wait_timer_duration = 30
        self.current_wait_timer = self.wait_timer_duration
        self.waiting_players = []
        self.joined_players = [bjp.Player.create_new_player_from_template('Alex')]
        self.known_players = [] # list of all players who have played a shoe, now or in the past
        self.active_player = None
        self.current_round_natural_blackjacks = {} # dictionary storing all naturally dealt blackjacks per player
        self.player_turn_actions = {
            'stand': lambda: self.stand(),
            'hit': lambda: self.hit(),
            'double down': lambda: self.double_down(),
            'split': lambda: self.split(),
            'surrender': lambda: self.surrender(),
            'insurance': lambda: self.insurance(),
            'even money': lambda: self.even_money()
        }
        self.player_special_actions = {
            'join': lambda: self.join(),
            'bet': lambda: self.bet(),
            'skip': lambda: self.skip_turn(),
            'leave': lambda: self.leave()
        }


    def transition(self, next_state):
        self.state = next_state


    # Player Turn Actions #    
    def stand(self):
        # Pass to next player
        if (self.active_player != self.joined_players[-1]):
            self.active_player = self.joined_players[self.joined_players.index(self.active_player)+1]
            self.transition(GameState.PLAYER_PLAYING)
        else:
            # If there is no next player, pass to dealer
            self.transition(GameState.DEALER_PLAYING)

    def hit(self, player):
        self.handle_front_cut_card()
        player.current_hands[0].extend([self.shoe.pop(0)])
        self.transition(GameState.SCORING)

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

    # Other Player Actions #
    def bet(self):
        pass
    
    def skip_turn(self):
        pass

    def join(self):
        pass

    def leave(self):
        pass


    # Debug #
    def dump_state_machine_data(self):
        print("*  *  *  *  *")
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
        print("*  *  *  *  *")

    def dump_shoe_data(self):
        print("*  *  *  *  *")
        print("START - DUMPING SHOE DATA")
        print('shoe_size:',len(self.shoe))
        print('discard_size:',len(self.discard))
        for attr, value in self.__dict__.items():
            if attr == 'shoe':
                print(attr+': '+str(value))
            elif attr == 'discard':
                print(attr+': '+str(value))
        print("END OF DUMPING SHOE DATA")
        print("*  *  *  *  *")

    def dump_state_mode(self):
        pass
    # Can use diff before/after a function call on generated text files
    # How to toggle this automatically w/o manually adding conditionals before/after?

    def print_missing_cards_in_single_deck_shoe_if_any(self):
        missing_cards = list(set(bjo.base_deck).difference(set(self.shoe)))
        if len(missing_cards) == 0:
            print("*** No cards missing in shoe ***")
        else:
            print("*  *  *  *  *")
            print(len(bjo.base_deck), "CARDS IN REFERENCE SINGLE DECK:")
            print(bjo.base_deck)
            print(len(self.shoe), "CARDS IN SHOE:")
            print(self.shoe)
            print("The following cards are missing -", missing_cards)
            print("*  *  *  *  *")

    def print_all_hands(self):
        print("*  *  *  *  *")
        print(self.dealer.name, "has a hand of", self.dealer.current_hands[0])
        for player in self.joined_players:
            if len(player.current_hands) <= 1:
                print(player.name, "has a hand of", player.current_hands[0])
            else:
                print(player.name, "has the following hands:", player.current_hands)
        print("*  *  *  *  *")

    def print_all_players_with_natural_blackjack_hands(self):
        for player in self.current_round_natural_blackjacks.keys():
            for hand in self.current_round_natural_blackjacks[player]:
                print(player.name,"has natural blackjack of", hand)



    # State Machine Actions #
    """
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
    """


    def start_game(self):
        print("STARTING GAME")
        # Initialize first player (sitting leftmost w.r.t. dealer) to be active
        self.active_player = self.joined_players[0]
        # Add all joined players to known
        # YOUR CODE HERE #
        self.dealer.print_player_stats()
        for player in self.joined_players:
            player.print_player_stats()
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

    
    def handle_front_cut_card(self):
        if ('front_cut_card' == self.shoe[0]):
            self.discard.extend([self.shoe.pop(0)])


    def score_all_joined_players_hands(self):
        # Score each player's hands
        for player in self.joined_players:
            for hand in player.current_hands:
                player_hand_score = bjl.highest_hand_score(hand)
                player.current_hand_scores.append(player_hand_score)
                if (player_hand_score == 21):
                    if (player not in self.current_round_natural_blackjacks.keys()):
                        self.current_round_natural_blackjacks[player] = [hand]
                    else:
                        self.current_round_natural_blackjacks[player].append(hand)
        self.print_all_players_with_natural_blackjack_hands()


        """
        for card in shoe_reference:
            if card[:-1] not in card_counts.keys():
                card_counts[card[:-1]] = [card]
            else:
                card_counts[card[:-1]].append(card)

        print(card_counts)
        """
        """
        # Score dealer's hand
        dealer_hand_score = bjl.highest_hand_score(self.dealer.current_hands[0])
        self.dealer.current_hand_scores.append(dealer_hand_score)
        """


    def check_for_and_handle_dealer_blackjack(self):
        dealer_face_up_card = self.dealer.current_hands[0][0]
        dealer_face_up_card_value = bjo.cards[dealer_face_up_card[:-1]][0]
        dealer_hole_card = self.dealer.current_hands[0][1]
        dealer_hole_card_value = bjo.cards[dealer_hole_card[:-1]][0]
        if (dealer_face_up_card in ['AH', 'AC', 'AD', 'AS']):
            print("Offering 'insurance' and 'even money' side bets")
            if (dealer_hole_card_value == 10):
                print("1. Reveal dealer hole card")
                print("Dealer hand is: ", self.dealer.current_hands[0])
                print("2. Pay out side bets to participating hands left-to-right, discard them")
                # Todo AB: PAY OUT ALL SIDE BETS TO PARTICIPATING HANDS LEFT-TO-RIGHT AND DISCARD THEM
                # YOUR CODE HERE #
                print("3. Push against all hands with Blackjack left-to-right, discard them")
                # Todo AB: ITERATE OVER ALL PLAYERS' BLACKJACK HANDS AND DISCARD THEM
                for blackjack_hand in self.current_round_natural_blackjacks:
                    pass

                print("4. Collect bets from all hands without side bets or Blackjack left-to-right, discard them")
                # Todo AB: ITERATE OVER ALL PLAYERS' NON-BLACKJACK HANDS AND DISCARD THEM

                print("5. Discard dealer hand and reset score")
                self.discard.extend(self.dealer.current_hands.pop(0))
                self.dealer.current_hand_scores.clear()
                print("ROUND END")
                self.transition(GameState.DEALING)
            else:
                print("Dealer doesn't have Blackjack!")
                print("Collecting side bets from all participating hands left-to-right")
                # Todo AB: COLLECT ALL SIDE BETS FROM PARTICIPATING HANDS LEFT-TO-RIGHT
                # YOUR CODE HERE #
                self.transition(GameState.PLAYER_PLAYING)
        elif (dealer_face_up_card_value == 10):
            if (dealer_hole_card in ['AH', 'AC', 'AD', 'AS']):
                print("1. Reveal dealer hole card")
                print("2. Push against all hands with Blackjack left-to-right, discard them")
                print("3. Collect bets from all players without side bets or Blackjack left-to-right, discard them")
                print("4. Discard dealer hand")
                print("ROUND END")
                self.transition(GameState.DEALING)
            else:
                print("Dealer doesn't have Blackjack!")
                self.transition(GameState.PLAYER_PLAYING)
        else:
            print("Dealer can't have Blackjack.")
            self.transition(GameState.PLAYER_PLAYING)


    def check_for_and_handle_players_blackjacks(self):
        if (self.num_of_naturally_dealt_blackjacks == 0):
            pass
        else:
            # Pay Blackjack to each natural hand
            pass

        """
        # Check if a player has only one hand and one score; process accordingly
        #self.print_all_hands()
        if (len(self.active_player.current_hands) == 1) and (len(self.active_player.current_hand_scores) == 1):
            if (self.active_player.current_hand_scores[0] == 21):
                # Payout Blackjack to all winning hands from left to right
                print("Blackjack!")
                self.transition(GameState.CLEANUP)
            elif (self.active_player.current_hand_scores[0]  == -1):
                print("Bust!")
                # Take bet associated /w hand
                # Put bust hand into discard
                pass
                #self.transition(GameState.CLEANUP)
            else:
                self.transition(GameState.PLAYER_PLAYING)
            print("Player score is:", self.active_player.current_hand_scores[0])
            return self.active_player.current_hand_scores[0]
        """


    def deal(self):
        for x in range(0, 2):
            # Deal a card to each player, then dealer, repeat once
            for player in self.joined_players:
                # Slide 'front_cut_card' to discard if encountered mid-shoe
                self.handle_front_cut_card()
                if len(player.current_hands) == 0:
                    player.current_hands.append([])
                player.current_hands[0].extend([self.shoe.pop(0)])
            # Slide 'front_cut_card' to discard if encountered mid-shoe
            self.handle_front_cut_card()
            if len(self.dealer.current_hands) == 0:
                self.dealer.current_hands.append([])
            self.dealer.current_hands[0].extend([self.shoe.pop(0)])
        # Print debug info on players hands and % of shoe dealt
        self.print_all_hands()
        self.dealer.print_player_stats()
        for player in self.joined_players:
            player.print_player_stats()
        print(str(int(round(100-(100*(len(self.shoe)/(2+self.num_of_decks*52))), 0)))+"%"+" of the shoe dealt "
            +"(reshuffling at round end past "+str(self.pen)+"%"+")")
        self.transition(GameState.SCORING)


    def player_plays(self):
        # Get action from currently active player (starting leftmost at hand start)
        self.active_player.action = input("Enter an action: ").strip().lower()
        # Check that active player action is valid
        if self.active_player.action not in self.player_turn_actions:
            print("Unknown action", repr(self.active_player.action), "from player", self.active_player.name,
                  "entered, please enter one of the following without quotes:")
            print(list(self.player_turn_actions.keys()))
        else:
            print("Executing Player "+self.active_player.name+"'s action "+repr(self.active_player.action))
            # Execute player's entered action
            self.player_turn_actions[self.active_player.action]()
            # Transitions are handled by each respective player action function


    def dealer_plays(self):
        if self.seventeen_rule == 'S17':
            while self.dealer.current_hand_scores[0] < 17:
                # Execute 'hit'
                self.hit(self.dealer)
            self.transition(GameState.ROUND_ENDING)
        elif self.seventeen_rule == 'H17':
            while self.dealer.current_hand_scores[0] <= 17:
                # Execute 'hit'
                self.hit(self.dealer)
            self.transition(GameState.ROUND_ENDING)
        # debug log and assert

        else:
            print("[ERR] Seventeen rule syntax not recognized")


    def round_end_cleanup(self):
        print("ROUND END")
        # Empty all players' hands by putting them in discard
        for player in self.joined_players:
            for hand_index in range(0, len(player.current_hands)):
                self.discard.extend(player.current_hands.pop(0))    
            # Reset all players' scores
            player.current_hand_scores.clear()
        # Empty dealer hand by putting it into discard
        self.discard.extend(self.dealer.current_hands.pop(0))
        # Reset dealer hand score
        self.dealer.current_hand_scores.clear()
        # Reshuffle at round end if 'front_cut_card' was reached
        if 'front_cut_card' in self.discard:
            print("SHOE END, reshuffling!")
            self.transition(GameState.SHUFFLING)
        else:
            self.transition(GameState.DEALING)


    def step(self):
        print(f"Current state: {self.state}")
        match self.state:
            case GameState.STARTING:
                self.start_game()
            case GameState.SHUFFLING:
                self.shuffle_cut_and_burn(None) # Todo: AB - pen % is different upon each reshuffle in a single session
            case GameState.DEALING:
                self.deal()
            case GameState.SCORING:
                self.score_all_joined_players_hands()

                self.check_for_and_handle_dealer_blackjack()
                self.check_for_and_handle_players_blackjacks()
            case GameState.PLAYER_PLAYING:
                self.player_plays()
            case GameState.DEALER_PLAYING:
                self.dealer_plays()
            case GameState.ROUND_ENDING:
                self.round_end_cleanup()
            case other:
                print("Invalid state!")
                raise NameError

    def run(self):
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