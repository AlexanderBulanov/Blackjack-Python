""" 
File: blackjack_fsm.py
Author: Alexander Bulanov
"""

# Global Imports #
import random
#import time
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
    BETTING = 2
    DEALING = 3
    INITIAL_SCORING = 4
    PLAYER_PLAYING = 5
    DEALER_PLAYING = 6
    RESCORING = 7
    ROUND_ENDING = 8


class BlackjackStateMachine:
    def __init__(self, num_of_decks):
        self.state = GameState.STARTING
        self.num_of_decks = num_of_decks
        self.pen = None
        self.shoe = bjo.get_shoe_of_n_decks(self.num_of_decks)
        self.discard = []
        self.dealer = bjp.Player.create_casino_dealer()
        self.seventeen_rule = 'S17'
        self.waiting_players = []
        self.joined_players = {1: None, 2: bjp.Player.create_new_player_from_template('Alex'), 3: None, 4: None, 5: None, 6: None, 7: None}
        self.known_players = [] # list of all players who have played a shoe, now or in the past
        self.active_player = None
        self.current_round_natural_blackjacks = {} # dictionary of players and all of their naturally dealt blackjack hands in a given round
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
            'color up': lambda: self.color_up(),
            'break down': lambda: self.break_down(),
            'bet': lambda: self.bet(),
            'skip': lambda: self.skip_turn(),
            'leave': lambda: self.leave()
        }


    def transition(self, next_state):
        self.state = next_state


    # Player Turn Actions #    
    def stand(self):
        next_player_present = False
        current_active_table_seat = 0
        # Get table seat of currently active player
        for joined_player in self.joined_players.values():
            current_active_table_seat += 1
            if (joined_player == self.active_player):
                break
        # Scan for another player sitting at a higher-indexed table seat
        for next_table_seat in range(current_active_table_seat+1, 8):
            next_player = self.joined_players[next_table_seat]
            # Assign next active player at a higher-indexed table seat
            if next_player != None:
                next_player_present = True
                self.active_player = next_player
                self.transition(GameState.PLAYER_PLAYING)
                break
        # No next player at higher-indexed table seat --> set leftmost (w.r.t dealer) player to be active
        if next_player_present == False:
            for joined_player in self.joined_players.values():
                if joined_player != None:
                    self.active_player = joined_player
                    break
            self.transition(GameState.DEALER_PLAYING)
            

    def hit(self, player):
        # Todo AB: Add hand_index as a variable to account for a single player playing multiple hands at a table
        self.handle_front_cut_card()
        player.current_hands[0].extend([self.shoe.pop(0)])
        self.transition(GameState.INITIAL_SCORING)

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
    def join(self):
        pass

    def color_up(self):
        pass

    def break_down(self):
        pass

    def bet(self, player, player_hand):
        # Create a dictionary containing 
        
        pass
    
    def skip_turn(self):
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
        for player in self.joined_players.values():
            if player != None:
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
        """
        # Manually create a test player and assign them to table spot 2
        player = bjp.Player.create_new_player_from_template('Alex')
        player.table_seat = 2
        self.joined_players[player.table_seat] = player
        """
        print("STARTING GAME WITH THE FOLLOWING PLAYERS:")
        for table_seat, joined_player in self.joined_players.items():
            if joined_player != None:
                print(joined_player.name, "at table seat", table_seat)
        # Initialize first player (sitting leftmost w.r.t. dealer) to be active
        for joined_player in self.joined_players.values():
            if joined_player != None:
                self.active_player = joined_player
                break
        # Add all new joined players to known
        for joined_player in self.joined_players.values():
            if joined_player != None:
                if joined_player not in self.known_players:
                    self.known_players.append(joined_player)

            """
            if given_player == None:
                continue
            else:
                if given_player not in self.known_players:
                    self.known_players.append(given_player)
            """
        """
        # DEBUG
        self.dealer.print_player_stats()
        for player in self.joined_players:
            player.print_player_stats()
        """
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
        self.transition(GameState.BETTING)

    

    def get_primary_player_bets(self): # Todo AB: Use threading package provided by Python
        player_responses = {player: None for player in self.joined_players.values()}
        #Poll players continously until you receive a response from each
        while None in player_responses.values():
            # Valid chip bet responses - bets using any combination of chips except for odd number of Pink ones
            # Other valid responses - bet using cash (???)
            # Other valid responses - skip, leave
            pass



    def handle_front_cut_card(self):
        if ('front_cut_card' == self.shoe[0]):
            self.discard.extend([self.shoe.pop(0)])


    def score_all_hands_in_play(self):
        for player in self.joined_players.values():
            if player != None:
                for hand in player.current_hands:
                    # Score each player's hands
                    player_hand_score = bjl.highest_hand_score(hand)
                    player.current_hand_scores.append(player_hand_score)
                    # Track natural blackjack hands for each player, as they're encountered
                    if (player_hand_score == 21):
                        if (player not in self.current_round_natural_blackjacks.keys()):
                            self.current_round_natural_blackjacks[player] = [hand]
                        else:
                            self.current_round_natural_blackjacks[player].append(hand)
        #self.print_all_players_with_natural_blackjack_hands()
        dealer_hand_score = bjl.highest_hand_score(self.dealer.current_hands[0])
        self.dealer.current_hand_scores.append(dealer_hand_score)

    def offer_insurance_and_even_money_side_bets(self):
        pass

    def reveal_dealer_hand(self):
        print("Dealer hand is: ", self.dealer.current_hands[0])

    def handle_winning_side_bet_hands(self):
        # Go through winning side bet hands left-to-right and pay winnings
        pass

    def handle_initial_blackjack_hand_pushes(self):
        for player in self.current_round_natural_blackjacks.keys():
            for hand_count in range(0, len(self.current_round_natural_blackjacks[player])):
                hand = self.current_round_natural_blackjacks[player][0]
                print("Dealer pushes against player", player.name, "with natural blackjack of", hand)
                # Remove player's leftmost blackjack hand from dictionary of natural blackjacks
                self.current_round_natural_blackjacks[player].remove(hand)
                # Push against player's bet
                
                # Todo AB: Iterate over player.current_primary_bets

                # USE A DICTIONARY TO STORE EACH BET
                # STORE ALL OF THE DICTIONARIES IN A LIST



                # Put player's leftmost blackjack hand into discard from hand
                self.discard.extend(player.current_hands.pop(player.current_hands.index(hand)))
                # Remove player's leftmost discarded blackjack hand score
                player.current_hand_scores.remove(21)

    def handle_losing_primary_bet_hands(self):
        # Go through losing primary bet hands left-to-right - collect bets, discard hands and reset their scores
        for player in self.joined_players.values():
            if player != None:
                for hand_count in range(0, len(player.current_hands)):
                    hand = player.current_hands[0]
                    dealer_blackjack = self.dealer.current_hands[0]
                    print(player.name, "loses with hand of", hand, "to Dealer's Blackjack of", dealer_blackjack)
                    # Todo AB: Collect player's leftmost hand bet

                    # Put player's leftmost hand into discard from hand
                    self.discard.extend(player.current_hands.pop(0))
                    # Remove player's leftmost hand score
                    player.current_hand_scores.pop(0)

    def reset_dealer_hand(self):
        self.discard.extend(self.dealer.current_hands.pop(0))
        self.dealer.current_hand_scores.clear()

    def handle_losing_side_bet_hands(self):
        # Go through losing side bet hands left-to-right and collect bets
        pass

    def handle_winning_primary_bet_hands(self):
        # Go through winning primary bet hands left-to-right - pay winnings, discard hands and reset their scores
        pass


    def check_for_and_handle_dealer_blackjack(self):
        dealer_face_up_card = self.dealer.current_hands[0][0]
        dealer_face_up_card_value = bjo.cards[dealer_face_up_card[:-1]][0]
        dealer_hole_card = self.dealer.current_hands[0][1]
        dealer_hole_card_value = bjo.cards[dealer_hole_card[:-1]][0]
        if (dealer_face_up_card in ['AH', 'AC', 'AD', 'AS']):
            print("Dealer's face-up card is an Ace!")
            print("Offering 'insurance' and 'even money' side bets:")
            self.offer_insurance_and_even_money_side_bets() # Todo AB: Add functionality to offer side bets
            if (dealer_hole_card_value == 10):
                self.reveal_dealer_hand()
                self.handle_winning_side_bet_hands() # Todo AB: Add functionality to pay out winning side bet hands
                self.handle_initial_blackjack_hand_pushes()
                self.handle_losing_primary_bet_hands()
                self.reset_dealer_hand()
                print("ROUND END")
                self.transition(GameState.BETTING)
            else:
                print("Dealer checks hole card - not a ten, doesn't have Blackjack.")
                self.handle_losing_side_bet_hands() # Todo AB: Add functionality to collect losing side bet hands
                self.transition(GameState.PLAYER_PLAYING)
        elif (dealer_face_up_card_value == 10):
            print("Dealer's face-up card is a ten!")
            if (dealer_hole_card in ['AH', 'AC', 'AD', 'AS']):
                self.reveal_dealer_hand()
                self.handle_initial_blackjack_hand_pushes()
                self.handle_losing_primary_bet_hands()
                self.reset_dealer_hand()
                print("ROUND END")
                self.transition(GameState.BETTING)
            else:
                print("Dealer checks hole card - not an Ace, doesn't have Blackjack.")
                self.transition(GameState.PLAYER_PLAYING)
        else:
            print("Dealer can't have Blackjack.")
            self.transition(GameState.PLAYER_PLAYING)


    def check_for_and_handle_players_blackjacks(self):
        if (len(self.current_round_natural_blackjacks.keys()) == 0):
            print("No players have natural Blackjack.")
            self.transition(GameState.PLAYER_PLAYING)
        else:
            print("Paying Blackjacks to each eligible player hand")
            self.handle_winning_primary_bet_hands()
            players_with_blackjacks = [player for player in self.current_round_natural_blackjacks.keys()]
            #print("Players /w Blackjack hands are:", players_with_blackjacks[0].name)
            for player in players_with_blackjacks:
                # Iterate over all Blackjack hands
                for hand_count in range(0, len(self.current_round_natural_blackjacks[player])):
                    hand = self.current_round_natural_blackjacks[player][0]
                    # Pay Blackjack to player
                    print("Paying Blackjack 3:2 to player", player.name, "with hand of", hand)
                    # Remove player's Blackjack hand from list of natural blackjacks for that player
                    if len(self.current_round_natural_blackjacks[player]) <= 1:
                        del self.current_round_natural_blackjacks[player]
                    else:
                        self.current_round_natural_blackjacks[player].remove(hand)
                    # Reset player's Blackjack hand score and discard it
                    print("Current hands for player", player.name, "are", player.current_hands)
                    print("Current hand scores for player", player.name, "are", player.current_hand_scores)
                    player.current_hand_scores.pop(player.current_hands.index(hand))
                    self.discard.extend(player.current_hands.pop(player.current_hands.index(hand)))
                    print("Updated hands for player", player.name, "are", player.current_hands)
                    print("Updated hand scores for player", player.name, "are", player.current_hand_scores)
            # Check if dealer's hand needs to be discarded due to all player hands being Blackjacks
            remaining_hands = 0
            for player in self.joined_players.values():
                if player != None:
                    remaining_hands += len(player.current_hands)
            if remaining_hands == 0:
                self.reset_dealer_hand()
                print("ROUND END")
                self.transition(GameState.DEALING)
            else:
                self.transition(GameState.PLAYER_PLAYING)
            """
            DEBUG:
            print("Current natural blackjacks:")
            print(self.current_round_natural_blackjacks)
            """


    def deal(self):
        for x in range(0, 2):
            # Deal a card to each player, then dealer, repeat once
            for player in self.joined_players.values():
                if player != None:
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
        """
        # DEBUG
        self.dealer.print_player_stats()
        for player in self.joined_players:
            player.print_player_stats()
        """
        self.print_all_hands()
        print(str(int(round(100-(100*(len(self.shoe)/(2+self.num_of_decks*52))), 0)))+"%"+" of the shoe dealt "
            +"(reshuffling at round end past "+str(self.pen)+"%"+")")
        self.transition(GameState.INITIAL_SCORING)


    def player_plays(self):
        """
        DEBUG
        """
        self.active_player.print_player_stats()
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
        initial_dealer_hand_score = self.dealer.current_hand_scores[0]
        if self.seventeen_rule == 'S17':
            print(self.seventeen_rule, "rule is in play")
            if (initial_dealer_hand_score >= 17):
                print("Dealer stands with a score of", initial_dealer_hand_score)
                self.transition(GameState.ROUND_ENDING)
            else:
                while (self.dealer.current_hand_scores[0] < 17) and (self.dealer.current_hand_scores[0] > 0):
                    # Execute 'hit'
                    print("Hitting Dealer's hand of", self.dealer.current_hands[0])
                    self.hit(self.dealer)
                    # Score the updated hand
                    new_dealer_hand_score = bjl.highest_hand_score(self.dealer.current_hands[0])
                    # Overwrite old score value with new one
                    self.dealer.current_hand_scores.clear()
                    self.dealer.current_hand_scores.append(new_dealer_hand_score)
                    print("Dealer's hand is now", self.dealer.current_hands[0],
                        "and has a score of", self.dealer.current_hand_scores[0])
                if (self.dealer.current_hand_scores[0] == 21):
                    print("Dealer hits Blackjack!")
                    print("Pushing against all players who match the dealer")
                    print("Collecting bets from all players who lose to dealer")
                elif (self.dealer.current_hand_scores[0] < 0):
                    print("Dealer busts!")
                    print("Paying all remaining in-play hands")
                else:
                    print("Dealer stands with a final score of", self.dealer.current_hand_scores[0])
            self.transition(GameState.ROUND_ENDING)
        elif self.seventeen_rule == 'H17':
            print(self.seventeen_rule, "rule is in play")
            if (initial_dealer_hand_score > 17):
                print("Dealer stands with a score of", initial_dealer_hand_score)
                self.transition(GameState.ROUND_ENDING)
            else:
                while (self.dealer.current_hand_scores[0] <= 17) and (self.dealer.current_hand_scores[0] > 0):
                    # Execute 'hit'
                    print("Hitting Dealer's hand of", self.dealer.current_hands[0])
                    self.hit(self.dealer)
                    # Score the updated hand
                    new_dealer_hand_score = bjl.highest_hand_score(self.dealer.current_hands[0])
                    # Overwrite old score value with new one
                    self.dealer.current_hand_scores.clear()
                    self.dealer.current_hand_scores.append(new_dealer_hand_score)
                    print("Dealer's hand is now", self.dealer.current_hands[0],
                        "and has a score of", self.dealer.current_hand_scores[0])
                if (self.dealer.current_hand_scores[0] < 0):
                    print("Dealer busts!")
                    print("Remaining players win!")
                else:
                    print("Dealer stands with a final score of", self.dealer.current_hand_scores[0])
                self.transition(GameState.ROUND_ENDING)
        # debug log and assert
        else:
            print("[ERR] Seventeen rule syntax not recognized")


    def round_end_cleanup(self):
        print("Paying all players who beat the dealer")
        print("Pushing against all players who match the dealer")
        print("Collecting bets from all players who lose to dealer")


        print("ROUND END")
        # Empty all players' hands by putting them in discard
        for player in self.joined_players.values():
            if player != None:
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
                self.shuffle_cut_and_burn(None) # Todo AB: pen % is different upon each reshuffle in a single session, need it fixed?
            case GameState.BETTING:
                self.transition(GameState.DEALING) # Todo AB: substitute in self.get_primary_player_bets()
            case GameState.DEALING:
                self.deal()
            case GameState.INITIAL_SCORING:
                self.score_all_hands_in_play()
                self.check_for_and_handle_dealer_blackjack()
                if (self.dealer.current_hands != []):
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