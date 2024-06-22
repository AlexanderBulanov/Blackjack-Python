""" 
File: blackjack_fsm.py
Author: Alexander Bulanov
"""

# Global Imports #
import random
import math
import msvcrt # used to get single character input from stdin
import sys # used for writing messages to stderr
#import time
from enum import Enum

# Local Imports #
from . import blackjack_game_logic as bjl
from . import blackjack_game_objects as bjo
from . import blackjack_players as bjp
from . import cut_helper as cut
from . import print_utils as prutils


### Blackjack State Machine ###
class GameState(Enum):
    INITIALIZING = 0
    WAITING = 1
    STARTING = 2
    SHUFFLING = 3
    BETTING = 4
    DEALING = 5
    INITIAL_SCORING = 6
    PLAYERS_PLAYING = 7
    DEALER_PLAYING = 8
    FINAL_SCORING = 9


class BlackjackStateMachine:
    def __init__(self, num_of_decks):
        self.state = GameState.INITIALIZING
        self.num_of_decks = num_of_decks
        self.pen = None # set in SHUFFLING within bounds specified for given num_of_decks
        self.shoe = bjo.get_shoe_of_n_decks(self.num_of_decks)
        self.discard = []
        self.min_bet = 1 # Options - 1 to 100
        self.max_bet = 100 # Options - 100 to 10000 (usually 100x the min_bet)
        self.blackjack_ratio = 3/2 # Options - 3/2, 6/5
        self.seventeen_rule = 'S17' # Options - 'S17', 'H17'
        self.surrender_rule = None # Options - None, 'ES', 'ES10', 'LS'
        self.doubling_rule = 'DA2' # Options - 'DA2', 'D9', 'D10'
        self.double_after_split_rule = 'DAS' # Options - 'DAS', 'NDAS'
        self.splitting_rule = 'SP4' # Options - 'SP2', 'SP4'
        self.split_10s_rule = 'Rank' # Options - 'Value', 'Rank'
        self.ace_resplit_rule = 'RSA' # Options - 'RSA', 'NRSA'
        self.unsupported_side_bet_shoe_size = 1 # single-deck shoes have no eligible side bets
        self.supported_side_bet_names = ['Perfect Pairs', 'Match the Dealer', 'Lucky Ladies', "King's Bounty", 'Buster Blackjack']
        self.supported_side_bet_limits = [(1, 100), (1, 500), (1, 25), (1, 100), (1, 100)]
        self.supported_side_bet_payout_tables = [
            {
             'Perfect Pair': 25,
             'Colored Pair': 12,
             'Red/Black Pair': 6
            },
            {
             '2 Suited Matches': 20,
             '1 Non-Suited & 1 Suited Match': 14,
             '1 Suited Match': 10,
             '2 Non-Suited Matches': 8,
             '1 Non-Suited Match': 4
            },
            {
             'Queen of Hearts Pair (with Dealer Blackjack)': 1000,
             'Queen of Hearts Pair': 125,
             'Matched 20': 19,
             'Suited 20': 9,
             'Unsuited 20': 4
            },
            {
             'King of Spades Pair (with Dealer Blackjack)': 1000,
             'King of Spades Pair': 100,
             'Suited Kings Pair (not spades)': 30,
             'Suited Qs, Js, or 10s Pair': 20,
             'Suited 20': 9,
             'Unsuited Kings Pair': 6,
             'Unsuited 20': 4
            },
            {
             '8 or More Cards': 250,
             '7 Cards': 50,
             '6 Cards': 12,
             '5 Cards': 4,
             '3 or 4 Cards': 2
            }
        ]
        self.table_side_bet_names = [] # Names of up to 2 supported side bets copied over in INITIALIZING state
        self.table_side_bet_limits = [] # Each side bet's limits are a tuple of (min_side_bet, max_side_bet); added in INITIALIZING state
        self.table_side_bet_payout_tables = [] # Tables of up to 2 supported side bets copied over in INITIALIZING state (optionally updated)

        self.joining_restriction = None # Options - None, 'NMSE'
        self.dealer = bjp.Player.create_casino_dealer()
        self.waiting_players = []
        self.seated_players = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
        self.known_players = [] # list of all players who have played a shoe, now or in the past
        self.active_player = None
        self.current_round_natural_blackjacks = {} # dictionary of players and all of the seats to which blackjack hands were naturally dealt this round
        self.player_turn_actions = {
            'stand': lambda: self.stand(),
            'hit': lambda: self.hit(),
            'double down': lambda: self.double_down(),
            'split': lambda: self.split(),
            'surrender': lambda: self.surrender(),
        }
        """
            'st': lambda: self.stand(),
            'ht': lambda: self.hit(),
            'dd': lambda: self.double_down(),
            'sp': lambda: self.split(),
            'es': lambda: self.early_surrender(),
            'ls': lambda: self.late_surrender(),
        }
        """
        self.player_special_actions = {
            'join': lambda: self.join(),
            'color up': lambda: self.color_up(),
            'break down': lambda: self.break_down(),
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
        for seated_player in self.seated_players.values():
            current_active_table_seat += 1
            if (seated_player == self.active_player):
                break
        # Scan for another player sitting at a higher-indexed table seat
        for next_table_seat in range(current_active_table_seat+1, 8):
            next_player = self.seated_players[next_table_seat]
            # Assign next active player at a higher-indexed table seat
            if next_player != None:
                next_player_present = True
                self.active_player = next_player
                self.transition(GameState.PLAYERS_PLAYING)
                break
        # No next player at higher-indexed table seat --> set leftmost (w.r.t dealer) player to be active
        if next_player_present == False:
            for seated_player in self.seated_players.values():
                if seated_player != None:
                    self.active_player = seated_player
                    break
            self.transition(GameState.DEALER_PLAYING)
            

    def hit(self, player, seat_name):
        # Todo AB: Add hand_index as a variable to account for a single player playing multiple hands at a table
        self.handle_front_cut_card()
        player.hands[seat_name].append([self.shoe.pop(0)])
        self.transition(GameState.INITIAL_SCORING)

    def double_down(self):
        pass

    def split(self):
        pass

    def surrender(self):
        pass

    # Other Player Actions #
    def join(self):
        pass

    def color_up(self):
        pass

    def break_down(self):
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

    def print_all_hands(self): # Update to work /w players having multiple hands
        print("*  *  *  *  *")
        print(f"{self.dealer.name} has a hand of {self.dealer.hands['center_seat']}")
        for player in self.seated_players.values():
            if (player != None):
                for seat_name, seat_number in player.occupied_seats.items():
                    if (seat_number != None):
                        print(f"{player.name} has a hand of {player.hands[seat_name]}")
                    else:
                        # Handle verbose flag 'v' here
                        pass
        print("*  *  *  *  *")

    def print_all_players_with_natural_blackjack_hands(self):
        for player in self.current_round_natural_blackjacks.keys():
            for hand in self.current_round_natural_blackjacks[player]:
                print(f"{player.name} has natural blackjack of {hand}")

    # State Machine Actions #
    def print_blackjack_table(self):
        seat_display_elements = []
        for seat_number, seated_player in self.seated_players.items():
            if (seated_player == None):
                seat_display_elements.append(seat_number)
            else:
                seat_display_elements.append(seated_player.name)
        top_row_num_chars = len(str(seat_display_elements[6])) + len(str(seat_display_elements[0])) + 4
        mid_row_num_chars = len(str(seat_display_elements[5])) + len(str(seat_display_elements[1])) + 4 + 2*5
        bot_row_num_chars = len(str(seat_display_elements[4])) + len(str(seat_display_elements[3])) + len(str(seat_display_elements[2])) + 6 + 11 + 12
        max_num_row_chars = max(top_row_num_chars, mid_row_num_chars, bot_row_num_chars)
        total_padding_spaces = max_num_row_chars+20
        print(f"|{'-'*(total_padding_spaces)}|")
        print(f"|{' '*int(math.floor((total_padding_spaces-7)/2 + 1))}Dealer{' '*int(math.floor((total_padding_spaces-7)/2 + 0.5))}|")
        print(f"|[{seat_display_elements[6]}]{' '*(total_padding_spaces-top_row_num_chars)}[{seat_display_elements[0]}]|")
        print(f"|{' '*5}[{seat_display_elements[5]}]{' '*(total_padding_spaces-mid_row_num_chars)}[{seat_display_elements[1]}]{' '*5}|")
        print(f"|{' '*11}[{seat_display_elements[4]}]", end='')
        print(f"{' '*int(math.floor((total_padding_spaces-bot_row_num_chars)/3 + 4))}[{seat_display_elements[3]}]{' '*int(math.floor((total_padding_spaces-bot_row_num_chars)/2 + 1))}", end='')
        print(f"[{seat_display_elements[2]}]{' '*11}|") # Todo AB: Line up seat_display_elements[3] /w 'Dealer' word in line 2
        print(f"|{'-'*(total_padding_spaces)}|")        


    def wait_for_players_to_join(self): # Pass-and-Play version
        print("Welcome to Pass-and-Play Casino Blackjack!")
        self.print_blackjack_table()
        print("Please enter your username and preferred seat out of those available above.")
        start_flag = False
        table_player_names = []
        remaining_seats = list(self.seated_players.keys())
        while (start_flag != 's'):
            new_player_username = input("Username: ")
            new_player_chosen_seat = None
            if new_player_username in table_player_names:
                sys.stderr.write(f"Name '{new_player_username}' has already been chosen by another player. Please enter a different username.\n")
            else:
                table_player_names.append(new_player_username)
                if (len(remaining_seats) == 1):
                    print(f"Only one seat available! Assigning seat {remaining_seats[0]} to player '{new_player_username}'")
                    new_player_chosen_seat = remaining_seats[0]
                    self.seated_players[new_player_chosen_seat] = bjp.Player.create_new_player_from_template(new_player_username, new_player_chosen_seat)
                    remaining_seats.pop(0) # All seats are now occupied
                else:
                    switch_to_next_player_flag = False # Flag to signal termination of while loop
                    while (switch_to_next_player_flag == False):
                        try:
                            seat_number_input = input("Preferred seat number: ")
                            new_player_chosen_seat = int(seat_number_input)
                            if new_player_chosen_seat not in remaining_seats:
                                print(f"Seat {new_player_chosen_seat} is already occupied by '{self.seated_players[new_player_chosen_seat].name}'. Please choose a different seat.")
                            else:
                                self.seated_players[new_player_chosen_seat] = bjp.Player.create_new_player_from_template(new_player_username, new_player_chosen_seat)
                                remaining_seats.pop(remaining_seats.index(new_player_chosen_seat))
                                switch_to_next_player_flag = True # Update the flag to get next player's input
                        except ValueError:
                            sys.stderr.write(f"Non-integer seat number '{seat_number_input}' provided. Please input an integer between 1 and 7\n")
                if (len(remaining_seats) > 0):
                    print("Press 'p' to pass the keyboard to the next player or 's' to start the game with the following currently seated players:")
                    self.print_blackjack_table()
                    switch_to_next_player_flag = False # Flag to signal termination of while loop
                else:
                    self.print_blackjack_table()
                    start_flag = 's'
                while (switch_to_next_player_flag == False):
                    key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
                    match key:
                        case 'p':
                            switch_to_next_player_flag = True
                            print("Please enter your username and preferred seat out of those available above.")
                        case 's':
                            switch_to_next_player_flag = True
                            start_flag = 's'
                        case other:
                            sys.stderr.write(f"Invalid input '{key}'\n")
                            print("Press 'p' to pass the keyboard to the next player or 's' to start the game with currently seated players")
        self.transition(GameState.STARTING)


    def start_game(self):
        print("STARTING GAME WITH THE FOLLOWING PLAYERS:")
        for table_seat, seated_player in self.seated_players.items():
            if seated_player != None:
                print(f"'{seated_player.name}' in seat #{table_seat}")
        # Initialize first player (sitting leftmost w.r.t. dealer) to be active
        for seated_player in self.seated_players.values():
            if seated_player != None:
                self.active_player = seated_player
                break
        # Add all new joined players to known
        for seated_player in self.seated_players.values():
            if seated_player != None:
                if seated_player not in self.known_players:
                    self.known_players.append(seated_player)
        """
        # DEBUG
        self.dealer.print_player_stats()
        for player in self.seated_players:
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



    # Todo AB: Get main and side bet for each given seat (max of 2 non-insurance side bets as those are offered only in INITIAL_SCORING)
    def get_bets_from_all_one_player_occupied_seats(self, player, min_bet, max_bet):
        for seat_name, seat_pos in player.occupied_seats.items():
            if (seat_pos != None): # Get each player's main bets from up to 3 seats they can occupy
                # Get player's main bet at their given seat
                player.init_main_bet_fields(seat_name)
                print(f"Player '{player.name}' placing a main bet at Seat #{seat_pos} (their '{seat_name}')")
                prutils.view_chip_betting_interface()
                player.print_player_chip_pool()
                while True: # Using this format instead of try-except and custom exception ExitBettingInterface, to pass tests
                    if player.get_bet_input_character(min_bet, max_bet, seat_name):
                        print("Exiting betting interface...")
                        break
                # Get user input of which side bet they would like to make (limit 2) or press SKIP
                
                #print(f"Player '{player.name}' placing a side bet at Seat #{seat_pos} (their '{seat_name}')")
                #prutils.view_side_bet_options_interface()

                # Get player's side bets at their given seat (up to 2 per seat)
                # PROMPT PLAYER TO PLACE A SIDE BET OUT OF OFFERED ONES (AND MENTION LIMIT IS 2) OR SKIP
                
                #self.init_side_bet_fields(seat_name)
                
                    # AFTER RESOLVING AN OFFERED SIDE BET, ASK IF PLAYER WANTS TO MAKE ANOTHER ONE (AND MENTION LIMIT IS 2) OR SKIP
                





    def get_all_players_bets(self):
        for seated_player in self.seated_players.values():
            if (seated_player != None):
                self.get_bets_from_all_one_player_occupied_seats(seated_player, self.min_bet, self.max_bet)
                #self.active_player.print_player_stats()
        self.transition(GameState.DEALING)


    def handle_front_cut_card(self):
        if ('front_cut_card' == self.shoe[0]):
            self.discard.extend([self.shoe.pop(0)])


    def score_all_hands_in_play(self):
        for player in self.seated_players.values():
            if player != None:
                # Score each player's hands
                for seat_name, seat_number in player.occupied_seats.items():
                    if (seat_number != None):
                        player_hand_score = bjl.highest_hand_score(player.hands[seat_name])
                        player.hand_scores[seat_name] = player_hand_score
                        # Track natural blackjack hands for each player, as they're encountered
                        if (player_hand_score == 21):
                            if (player not in self.current_round_natural_blackjacks.keys()):
                                self.current_round_natural_blackjacks[player] = [seat_name]
                            else:
                                self.current_round_natural_blackjacks[player].append(seat_name)
        #self.print_all_players_with_natural_blackjack_hands()
        dealer_hand_score = bjl.highest_hand_score(self.dealer.hands['center_seat'])
        self.dealer.hand_scores['center_seat'] = dealer_hand_score


    def offer_insurance_and_even_money_side_bets(self):
        pass

    def reveal_dealer_hand(self):
        print(f"Dealer hand is {self.dealer.hands['center_seat']}")


    def reset_natural_blackjack_tracking(self): # Removes all natural player blackjacks from being tracked this round
        for player in self.current_round_natural_blackjacks.keys():
            #print(f"Dealer pushes against player {player.name} with natural blackjack of {hand})
            self.current_round_natural_blackjacks[player].clear()


    # Collects just one losing bet from a player - an example would be collecting player's losing side bet before game goes on /w their main bet still in play
    def collect_losing_player_bet(self, player, seat_name, bet_type):
        if seat_name not in ['right_seat', 'center_seat', 'left_seat']:
            sys.stderr.write(f"Invalid seat_name '{seat_name}' provided! Valid seat names are 'right_seat', 'center_seat', and 'left_seat'")
        if bet_type in ['main', 'side']:
            bets_name = bet_type + '_bets'
            player_chip_bet = getattr(player, bets_name)[seat_name] # player.main_bets[seat_name] OR player.side_bets[seat_name]
            if player_chip_bet != None:
                for chip_color, chip_count in player_chip_bet.items():
                    # Move bet chips from Player to Dealer and update Dealer's balance
                    chip_value = bjo.chips[chip_color]
                    self.dealer.chips[chip_color] += chip_count
                    self.dealer.chip_pool_balance += chip_count*chip_value
                self.dealer.cast_whole_number_chip_pool_balance_to_int()
                # Reset losing player's bet
                getattr(player, bets_name)[seat_name] = None # player.main_bets[seat_name] OR player.side_bets[seat_name]
                bet_amounts_name = bet_type + '_bet_amounts'
                getattr(player, bet_amounts_name)[seat_name] = None # player.main_bet_amounts[seat_name] OR player.side_bet_amounts[seat_name]
                # No need to subtract chips and chip_pool_balance for Player - already done when a bet is submitted
            else:
                sys.stderr.write(f"Player chip bet is {None}! Chip transfer from player '{player.name}' to Dealer cannot be completed.")
        else:
            sys.stderr.write(f"Invalid bet type provided! Valid bet types are either 'main' or 'side'")


    def collect_losing_main_bets(self):
        # Go through main bet hands left-to-right from dealer's POV and collect losing main bets
        # Note: Player model is structured in order from rightmost to leftmost player hand, allowing to simply iterate over occupied_seats
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        print(f"Player '{player.name}' loses with hand of {player.hands[seat_name]} to Dealer's Blackjack of {self.dealer.hands['center_seat']}")
                        self.collect_losing_player_bet(player, seat_name, 'main')


    def collect_losing_side_bets(self):
        # Go through side bet hands left-to-right from dealer's POV and collect losing side bets
        # Note: Player model is structured in order from rightmost to leftmost player hand, allowing to simply iterate over occupied_seats
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        print(f"Player '{player.name}' loses side bet of hand {player.hands[seat_name]} to Dealer")
                        self.collect_losing_player_bet(player, seat_name, 'side')


    # Possible to follow similar structure to losing bets above?
    def pay_winning_player_bet(self, player, seat_name, bet_type):
        pass

    # Todo AB: fix pay_winning_main_bets() to be functional and unit-test it
    def pay_winning_main_bets(self):
        # Go through main bet hands left-to-right from dealer's POV and pay winning main bets
        if self.state == GameState.INITIAL_SCORING:
            #players_with_blackjacks = [player for player in self.current_round_natural_blackjacks.keys()]
            #print("Players /w Blackjack hands are:", players_with_blackjacks[0].name)
            for player in self.current_round_natural_blackjacks.keys():
                player_blackjack_seat_names = self.current_round_natural_blackjacks[player]
                for seat_name in player_blackjack_seat_names:
                    remaining_payout = player.main_bet_amounts[seat_name] * self.blackjack_ratio
                    # Rounding only applies to 6:5 Blackjack payout ratio
                    if self.blackjack_ratio == 1.2:
                        remaining_payout = round(remaining_payout)
                        print(f"Paying Blackjack 6:5 to player {player.name} with hand of {player.hands[seat_name]}")
                    else:
                        print(f"Paying Blackjack 3:2 to player {player.name} with hand of {player.hands[seat_name]}")
                    # In regular (3:2) payout ratio, fractional .5 payouts always involve a Pink chip
                    if (type(remaining_payout) == float):
                        self.dealer.chips['Pink'] -= 1
                        self.dealer.chip_pool_balance -= 2.5
                        self.dealer.clean_up_fractions('center_seat') # WILL THIS MESS UP EXISTING FRACTIONAL BALANCE?
                        player.chips['Pink'] += 1
                        player.chip_pool_balance += 2.5
                        player.clean_up_fractions(seat_name) # WILL THIS MESS UP EXISTING FRACTIONAL BALANCE?

                        remaining_payout -= 1*2.5
                        remaining_payout = int(remaining_payout)
                    # Pay remaining part of winnings, if any
                    if (remaining_payout != 0):
                        for chip_name, chip_value in bjo.reverse_chips.items():
                            if chip_name != 'Pink':
                                remainder = remaining_payout % chip_value
                                if (remainder in range(0, remaining_payout)):
                                    chip_count = math.floor(remaining_payout/chip_value)
                                    self.transfer_main_bet_chips_and_update_balance(self.dealer, 'center_seat', player)

                                    self.dealer.chips[chip_name] -= chip_count
                                    self.dealer.chip_pool_balance -= chip_count*chip_value
                                    self.dealer.clean_up_fractions('center_seat') # WILL THIS MESS UP EXISTING FRACTIONAL BALANCE?
                                    player.chips[chip_name] += chip_count
                                    player.chip_pool_balance += chip_count*chip_value
                                    player.clean_up_fractions(seat_name) # WILL THIS MESS UP EXISTING FRACTIONAL BALANCE?

                                    remaining_payout -= chip_count*chip_value
                                    if (remaining_payout == 0):
                                        break
                    """
                    # Move all of the chips from player's bet at seat_name to dealer.chips
                    for chip_color, chip_count in player.main_bets[seat_name].items():
                        self.dealer.chips[chip_color] += chip_count
                        player.main_bets[seat_name][chip_color] -= chip_count
                    # Update dealer.chip_pool_balance
                    self.dealer.chip_pool_balance += player.main_bet_amounts[seat_name]
                    self.dealer.clean_up_fractions('center_seat')
                    player.main_bet_amounts[seat_name] = 0
                    """
        elif self.state == GameState.FINAL_SCORING:
            pass


    def pay_winning_side_bets(self):
        # Go through side bet hands left-to-right from dealer's POV and collect losing side bets
        # Note: Player model is structured in order from rightmost to leftmost player hand, allowing to simply iterate over occupied_seats
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        print(f"Player '{player.name}' wins side bet of hand {player.hands[seat_name]} to Dealer")
                        self.pay_winning_player_bet(player, seat_name, 'side')


    def discard_all_hands_in_play_and_reset_all_hand_scores(self):
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        self.discard.extend(player.hands['center_seat'])
                        player.hands['center_seat'].clear()
                        player.hand_scores[seat_name] = 0
        self.discard.extend(self.dealer.hands['center_seat'])
        self.dealer.hands['center_seat'].clear()
        self.dealer.hand_scores['center_seat'] = 0


    def check_for_and_handle_initial_dealer_blackjack_if_present(self):
        dealer_face_up_card = self.dealer.hands['center_seat'][0]
        dealer_hole_card = self.dealer.hands['center_seat'][1]
        dealer_face_up_card_value = bjo.cards[dealer_face_up_card[:-1]][0] # Used only to check if face card is 10/face, gives incorrect Ace value on purpose
        dealer_hole_card_value = bjo.cards[dealer_hole_card[:-1]][0] # Used only to check if hole card is 10/face, gives incorrect Ace value on purpose
        
        # Todo AB: OFFER EARLY SURRENDER HERE IF TABLE RULE ALLOWS IT

        if (dealer_face_up_card in ['AH', 'AC', 'AD', 'AS']):
            print("Dealer's face card is an Ace!")
            print("Offering 'insurance' and 'even money' side bets:")
            self.offer_insurance_and_even_money_side_bets() # Todo AB: Add functionality to offer side bets
            if (dealer_hole_card_value == 10):
                self.reveal_dealer_hand()
                self.pay_winning_side_bets() # Todo AB: Add functionality to pay out winning side bet hands
                self.reset_natural_blackjack_tracking()
                self.collect_losing_main_bets() # Todo AB: Test functionality of collecting losing main bets
                self.discard_all_hands_in_play_and_reset_all_hand_scores()
                print("ROUND END")
                self.transition(GameState.BETTING)
            else:
                print("Dealer checks hole card - not a ten, doesn't have Blackjack.")
                self.collect_losing_side_bets() # Todo AB: Test functionality of collecting losing side bets
        elif (dealer_face_up_card_value == 10):
            print("Dealer's face card is a ten!")
            if (dealer_hole_card in ['AH', 'AC', 'AD', 'AS']):
                self.reveal_dealer_hand()
                self.reset_natural_blackjack_tracking()
                self.collect_losing_main_bets() # Todo AB: Test functionality of collecting losing main bets
                self.discard_all_hands_in_play_and_reset_all_hand_scores()
                print("ROUND END")
                self.transition(GameState.BETTING)
            else:
                print("Dealer checks hole card - not an Ace, doesn't have Blackjack.")
        else:
            print("Dealer can't have Blackjack.")


    def check_for_and_handle_initial_players_blackjacks_if_any_present(self):
        if (len(self.current_round_natural_blackjacks.keys()) == 0):
            print("No players have natural Blackjack.")
            self.transition(GameState.PLAYERS_PLAYING)
        else:
            print("Paying Blackjacks to each eligible player hand")
            self.reveal_dealer_hand()
            self.pay_winning_main_bets()
            self.reset_natural_blackjack_tracking()


            
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
            for player in self.seated_players.values():
                if player != None:
                    for seat_name, seat_number in player.occupied_seats.items():
                        if seat_number != None:
                            if len(player.hands[seat_name]) == 2:
                                remaining_hands += 1
            if remaining_hands == 0:
                self.discard_all_hands_in_play_and_reset_all_hand_scores()
                print("ROUND END")
                self.transition(GameState.BETTING)
            else:
                self.transition(GameState.PLAYERS_PLAYING)


    def deal(self):
        # Repeat the following twice:
        for x in range(0, 2):
            # Deal a card from shoe to each player
            for player in self.seated_players.values():
                if (player != None):
                    for seat_name, seat_number in player.occupied_seats.items():
                        if (seat_number != None):
                            self.handle_front_cut_card() # Slide 'front_cut_card' to discard if encountered mid-shoe
                            if (player.hands[seat_name] == None):
                                player.hands[seat_name] = []
                            player.hands[seat_name].append(self.shoe.pop(0))
            # Deal a card from shoe to dealer
            self.handle_front_cut_card() # Slide 'front_cut_card' to discard if encountered mid-shoe
            if (self.dealer.hands['center_seat'] == None):
                self.dealer.hands['center_seat'] = []
            self.dealer.hands['center_seat'].append(self.shoe.pop(0))
        # Print debug info on players hands and % of shoe dealt
        """
        # DEBUG
        self.dealer.print_player_stats()
        for player in self.seated_players:
            player.print_player_stats()
        """
        self.print_all_hands()
        percentage_of_shoe_dealt = int(round(100-(100*(len(self.shoe)/(2+self.num_of_decks*52))), 0))
        print(f"{percentage_of_shoe_dealt}% of the shoe dealt (reshuffling at round end past {str(self.pen)}%)")
        self.transition(GameState.INITIAL_SCORING)


    def play_all_remaining_players_hands(self):
        for player in self.seated_players.values():
            if (player != None):
                for seat_name, seat_number in player.occupied_seats.items():
                    if (seat_number != None):
                        print(f"Player '{player.name}' chooses action at Seat #{seat_number} (their '{seat_name}')")
                        self.play_player_hand(player, seat_name)

    def play_player_hand(self, player, seat_name):
        #print(f"{player.name} has a hand of {player.hands[seat_name]}")
        # Get action from currently active player (starting leftmost at hand start)
        player.action = input("Enter an action: ").strip().lower()
        # Check that active player action is valid
        if player.action not in self.player_turn_actions:
            sys.stderr.write("Unknown action", repr(player.action), "from player", player.name,
                  "entered, please enter one of the following without quotes:\n")
            print(list(self.player_turn_actions.keys()))
        elif player.action == 'stand':
            print(f"Executing action '{player.action}' for player '{player.name}'")
            # Execute player's entered action
            self.player_turn_actions[player.action]()
            # Transitions are handled by each respective player action function
        else:
            # Process:
            # HIT
            # DOUBLE
            # SPLIT
            # LATE SURRENDER
            pass


    def dealer_plays(self):
        initial_dealer_hand_score = self.dealer.hand_scores['center_seat']
        if self.seventeen_rule == 'S17':
            print(f"{self.seventeen_rule} rule is in play")
            if (initial_dealer_hand_score >= 17):
                print(f"Dealer stands with a score of {initial_dealer_hand_score}")
                self.transition(GameState.ROUND_ENDING)
            else:
                while (self.dealer.hand_scores['center_seat'] < 17) and (self.dealer.hand_scores['center_seat'] > 0):
                    # Execute 'hit'
                    print(f"Hitting Dealer's hand of {self.dealer.hands['center_seat']}")
                    self.hit(self.dealer, 'center_seat')
                    # Score the updated hand
                    new_dealer_hand_score = bjl.highest_hand_score(self.dealer.hands['center_seat'])
                    # Overwrite old score value with new one
                    self.dealer.hand_scores['center_seat'].clear()
                    self.dealer.hand_scores['center_seat'].append(new_dealer_hand_score)
                    print("Dealer's hand is now", self.dealer.hands['center_seat'],
                        "and has a score of", self.dealer.hand_scores['center_seat'])
                if (self.dealer.hand_scores['center_seat'] == 21):
                    print("Dealer hits Blackjack!")
                    print("Pushing against all players who match the dealer")
                    print("Collecting bets from all players who lose to dealer")
                elif (self.dealer.hand_scores['center_seat'] < 0):
                    print("Dealer busts!")
                    print("Paying all remaining in-play hands")
                else:
                    print("Dealer stands with a final score of", self.dealer.hand_scores['center_seat'])
            self.transition(GameState.ROUND_ENDING)
        elif self.seventeen_rule == 'H17':
            print(f"{self.seventeen_rule} rule is in play")
            if (initial_dealer_hand_score > 17):
                print(f"Dealer stands with a score of {initial_dealer_hand_score}")
                self.transition(GameState.ROUND_ENDING)
            else:
                while (self.dealer.hand_scores['center_seat'] <= 17) and (self.dealer.hand_scores['center_seat'] > 0):
                    # Execute 'hit'
                    print(f"Hitting Dealer's hand of {self.dealer.hands['center_seat']}")
                    self.hit(self.dealer, 'center_seat')
                    # Score the updated hand
                    new_dealer_hand_score = bjl.highest_hand_score(self.dealer.hands['center_seat'])
                    # Overwrite old score value with new one
                    self.dealer.hand_scores['center_seat'].clear()
                    self.dealer.hand_scores['center_seat'].append(new_dealer_hand_score)
                    print("Dealer's hand is now", self.dealer.hands['center_seat'],
                        "and has a score of", self.dealer.hand_scores['center_seat'])
                if (self.dealer.hand_scores['center_seat'] < 0):
                    print("Dealer busts!")
                    print("Remaining players win!")
                else:
                    print("Dealer stands with a final score of", self.dealer.hand_scores['center_seat'])
                self.transition(GameState.ROUND_ENDING)
        # debug log and assert
        else:
            sys.stderr.write("[ERROR] Seventeen rule syntax not recognized\n")


    def check_for_and_handle_final_dealer_blackjack_if_present():
        pass


    def check_for_and_handle_final_players_blackjacks_if_any_present():
        pass


    def round_end_cleanup(self):
        print("Paying all players who beat the dealer")
        print("Pushing against all players who match the dealer")
        print("Collecting bets from all players who lose to dealer")

        # Todo AB: Reset appropriate player fields back to None

        print("ROUND END")
        # Empty all players' hands by putting them in discard
        for player in self.seated_players.values():
            if player != None:
                for hand_index in range(0, len(player.current_hands)):
                    self.discard.extend(player.current_hands.pop(0))    
                # Reset all players' scores
                player.current_hand_scores.clear()
        # Reset dealer's hand and hand score
        self.reset_dealer_hand_and_hand_score()
        # Reshuffle at round end if 'front_cut_card' was reached
        if 'front_cut_card' in self.discard:
            print("SHOE END, reshuffling!")
            self.transition(GameState.SHUFFLING)
        else:
            self.transition(GameState.DEALING)

    """
    def get_game_option_input_character(self):
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                self.view_game_launch_options()
            case 'd':
                self.print_player_chip_pool()
            case 'p':
                self.print_current_bet(seat)
            case 'r':
                self.reset_current_bet(seat)
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide a valid key or press 'v' to see valid key input options")
    """


    def step(self):
        print(f"Current state: {self.state}")
        match self.state:
            case GameState.INITIALIZING:
                print(f"Welcome to Blackjack! Please select game launch options from the ones listed below.")
                prutils.view_game_launch_options()




                #game_launch_option = self.get_game_option_input_character()

                
                
                # 1a. Ask user if they want to run a default game (/w option to adjust settings and deviate from template)
                # OR
                # 1b. Ask user if they want to load a game preset JSON file (/w option to adjust settings and deviate from preset)
                # OR
                # 1c. Ask user to manually specify all game settings
                # THEN
                # 2. Create a Blackjack table /w specified settings
                self.transition(GameState.WAITING)
            case GameState.WAITING:
                self.wait_for_players_to_join()
            case GameState.STARTING:
                for player in self.seated_players.values():
                    if (player != None):
                        player.print_player_stats()
                self.start_game()
            case GameState.SHUFFLING:
                self.shuffle_cut_and_burn(None) # Todo AB: pen % is different upon each reshuffle in a single session, need it fixed?
            case GameState.BETTING:
                self.get_all_players_bets() # Todo AB: update get_all_players_bets() to work /w players occupying multiple seats
            case GameState.DEALING:
                self.deal() # Todo AB: Update deal() to work with players occupying multiple seats
            case GameState.INITIAL_SCORING:
                self.score_all_hands_in_play()
                self.check_for_and_handle_initial_dealer_blackjack_if_present()
                if (self.dealer.hands['center_seat'] != []): # Happens only when dealer doesn't have blackjack
                    self.check_for_and_handle_initial_players_blackjacks_if_any_present()
            case GameState.PLAYERS_PLAYING:
                self.play_all_remaining_players_hands()
            case GameState.DEALER_PLAYING:
                self.dealer_plays()
            case GameState.FINAL_SCORING:
                self.check_for_and_handle_final_dealer_blackjack_if_present()
                if (self.dealer.hands['center_seat'] != []): # Happens only when dealer doesn't have blackjack
                    self.check_for_and_handle_final_players_blackjacks_if_any_present()
            case other:
                sys.stderr.write(f"Invalid state '{self.state}'!\n")
                raise NameError

    def run(self):
        try:
            while True:
                self.step()
        except KeyboardInterrupt:
                print("\nExiting state machine...")



"""
def add_state(self, prev_state, next_state, transition_condition, transition_output):
    self.state = next_state

def add_transition(self, start_state, end_state):
    # How to store transitions?
    #self.state = end_state
    pass
"""