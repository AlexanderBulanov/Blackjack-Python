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
    WAITING = 0
    STARTING = 1
    SHUFFLING = 2
    BETTING = 3
    DEALING = 4
    PRE_SCORING = 5
    INITIAL_SCORING = 6
    PLAYERS_PLAYING = 7
    DEALER_PLAYING = 8
    FINAL_SCORING = 9


class BlackjackStateMachine:
    def __init__(self, num_of_decks):
        self.state = GameState.WAITING
        self.num_of_decks = num_of_decks
        self.pen = None # set in SHUFFLING within bounds specified for given num_of_decks
        self.shoe = bjo.get_shoe_of_n_decks(self.num_of_decks)
        self.discard = []
        self.min_table_bet = 1 # Options - 1 to 100
        self.max_table_bet = 100 # Options - 100 to 10000 (usually 100x the min_bet)
        self.blackjack_ratio = 3/2 # Options - 3/2, 6/5
        self.seventeen_rule = 'H17' # Options - 'S17', 'H17'
        self.surrender_rule = 'LS' # Options - 'NS', 'ES', 'ES10', 'LS'
        self.doubling_rule = 'DA2' # Options - 'DA2', 'D9', 'D10'
        self.double_after_split_rule = 'DAS' # Options - 'DAS', 'NDAS'
        self.splitting_rule = 'SP4' # Options - 'SP2', 'SP4'
        self.split_10s_rule = 'Rank' # Options - 'Value', 'Rank'
        self.ace_resplit_rule = 'RSA' # Options - 'RSA', 'RSA3', 'NRSA'
        self.unsupported_side_bet_shoe_size = 1 # single-deck shoes have no eligible side bets
        self.supported_side_bet_names = ["Perfect Pairs", "Match the Dealer", "Lucky Ladies", "King's Bounty", "Buster Blackjack"]
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
        self.table_active_side_bet_names = ["Perfect Pairs", "Match the Dealer"] # Names of up to 2 supported side bets copied over in INITIALIZING state
        self.table_active_side_bet_limits = [(1, 100), (1, 500)] # Each side bet's limits are a tuple of (min_side_bet, max_side_bet); added in INITIALIZING state
        self.table_active_side_bet_payout_tables = [
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
            }
        ] # Tables of up to 2 supported side bets copied over in INITIALIZING state (optionally updated)
        self.joining_restriction = 'NMSE' # Options - None, 'NMSE'
        self.dealer = bjp.Player.create_casino_dealer()
        self.waiting_players = []
        self.seated_players = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
        self.known_players = [] # list of all players who have played a shoe, now or in the past
        self.last_occupied_seat = None
        self.active_player = None
        self.current_round_natural_blackjacks = {} # dictionary of players and all of their seats at which blackjack hands were naturally dealt this round ('center_seat', etc.)
        self.current_round_placed_side_bets_1 = {} # dictionary of players and all of their seats at which they placed a bet on Side Bet #1
        self.current_round_placed_side_bets_2 = {} # dictionary of players and all of their seats at which they placed a bet on Side Bet #2
        self.current_round_remaining_player_hands = None
        self.player_turn_actions = ['stand', 'hit', 'double', 'split', 'surrender']
        self.side_bet_handlers = {
            "Perfect Pairs": lambda player, seat_name: self.handle_perfect_pairs_side_bet(player, seat_name),
            "Match the Dealer": lambda player, seat_name: self.handle_match_the_dealer_side_bet(player, seat_name),
            "Lucky Ladies": lambda player, seat_name: self.handle_lucky_ladies_side_bet(player, seat_name),
            "King's Bounty": lambda player, seat_name: self.handle_kings_bounty_side_bet(player, seat_name),
            "Buster Blackjack": lambda player, seat_name: self.handle_buster_blackjack_side_bet(player, seat_name),
        }
        

    def transition(self, next_state):
        self.state = next_state

    # Player Turn Actions #    
    def stand(self, player):
        return True
            

    def hit(self, player, seat_name):
        # Todo AB: Add hand_index as a variable to account for a single player playing multiple hands at a table
        self.handle_front_cut_card()
        player.hands[seat_name].append([self.shoe.pop(0)])

        # Rescore hand internally after hit - if bust, return True
        #return True

        #self.transition(GameState.INITIAL_SCORING)

    def double(self):
        # Rescore hand internally after double - if bust, return True
        #return True
        pass

    def split(self):
        pass

    def surrender(self):
        # Collect player's hand and half of bet, then return True
        #return True
        pass


    # Other Player Actions #
    def color_up(self, player):
        print("Colored up chips!")
        pass

    def break_down(self, player):
        print("Broke down chips!")
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
            for seat_name in self.current_round_natural_blackjacks[player]:
                print(f"{player.name} has natural blackjack of {player.hands[seat_name]}")

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
        #self.print_blackjack_table()
        #print("Please enter your username and preferred seat(s) out of those available above.")
        player_seats_chosen_flag = False
        table_player_names = []
        remaining_seats = list(self.seated_players.keys())
        while (player_seats_chosen_flag == False):
            # Get new player's username
            new_player_username = input("Please enter your preferred username: ")
            new_player_chosen_seat = None
            if new_player_username in table_player_names:
                sys.stderr.write(f"Name '{new_player_username}' has already been chosen by another player. Please enter a different username.\n")
            else:
                table_player_names.append(new_player_username)
                # Automatically sit new player at the only available seat at the Blackjack table and start the game
                if (len(remaining_seats) == 1):
                    self.print_blackjack_table()
                    print(f"Only one seat available! Assigning seat {remaining_seats[0]} to player '{new_player_username}'")
                    new_player_chosen_seat = remaining_seats[0]
                    self.seated_players[new_player_chosen_seat] = bjp.Player.create_new_player_from_template(new_player_username, new_player_chosen_seat)
                    remaining_seats.pop(0) # All seats are now occupied
                    player_seats_chosen_flag = True
                else:
                    # 1. Print current state of the table
                    self.print_blackjack_table()
                    # 2. Print seat selection controls
                    prutils.view_seat_selection_interface()
                    # 3. Get user input (select seat, de-select seat, or confirm selection)
                    # 3a. Upon confirming selection, if player chose 2 seats, ask them to pick which seat they will physically sit at
                    # 3b. Handle errors:
                    # 3ba. choosing non-adjacent seats
                    # 3bb. removing a center seat out of 3 chosen, such that 2 remaining will be non-adjacent
                    # 3bc. choosing more than 3 seats
                    # 3bd. confirming selection with 0 seats
                    # 3be. confirming selection with 2 seats wo specifying center seat
                    # 3bf. 


                    print(f"Enter up to 3 preferred unoccupied seat positions (1-7) you would like to play hands from. Press 'f' when finished.")
                    chosen_adjacent_seats = []
                    while len(chosen_adjacent_seats) < 3:
                        print("Preferred seat: ")
                        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
                        if key == 'f':
                            pass


            # Create new player with chosen seats, as well as preferred center seat (when 2 are chosen)


        self.transition(GameState.STARTING)


    """
    def wait_for_players_to_join(self): # Pass-and-Play version
        print("Welcome to Pass-and-Play Casino Blackjack!")
        self.print_blackjack_table()
        print("Please enter your username and preferred seat(s) out of those available above.")
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
                # Get up to 3 adjacent seats at the table new player would like to play hands from
                else:
                    switch_to_next_player_flag = False # Flag to signal termination of while loop
                    while (switch_to_next_player_flag == False):
                        try:
                            print(f"Enter up to 3 preferred adjacent seats (#1-7) you would like to play hands from. Press 'f' when finished.")
                            chosen_adjacent_seats = []
                            while len(chosen_adjacent_seats) < 3:
                                print("Preferred seat: ")
                                input = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
                                if input == 'f':
                                    if len(chosen_adjacent_seats) == 0:
                                        print("Enter at least 1 seat at the table before pressing 'f'.")
                                    else:
                                        if len(chosen_adjacent_seats) == 2:
                                            print("Which seat would you like to sit at (not just play hand from) at the table?")
                                            print("Preferred seat: ")
                                            center_seat = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
                                            if center_seat not in chosen_adjacent_seats:
                                                print(f"Please enter a valid seat to sit at, out of your chosen seats of {chosen_adjacent_seats}")
                                            else:
                                                self.seated_players[center_seat] = bjp.Player.create_new_player_from_template(new_player_username, new_player_chosen_seat)
                                                remaining_seats.pop(remaining_seats.index(center_seat))
                                                switch_to_next_player_flag = True # Update the flag to get next player's input

                                        switch_to_next_player_flag = True # Update the flag to get next player's input
                                elif input in ['1', '2', '3', '4', '5', '6', '7']:
                                    pass
                                else:
                                    print("Invalid input - enter additional adjacent seats (#1-7) or press 'f' to finish selection.")





                            if new_player_chosen_seat not in remaining_seats:
                                print(f"Seat {new_player_chosen_seat} is already occupied by '{self.seated_players[new_player_chosen_seat].name}'. Please choose a different seat.")
                            elif not isAdjacent(new_player_chosen_seat, chosen_adjacent_seats):
                                print(f"Chosen seat {new_player_chosen_seat} is not adjacent to your other preferred seats. 
                                      Please make a different selection or press 'f' to finish choosing.")
                            else:
                                chosen_adjacent_seats.append(new_player_chosen_seat)


                                pass
                            """
    """
                            elif ():
                                self.seated_players[new_player_chosen_seat] = bjp.Player.create_new_player_from_template(new_player_username, new_player_chosen_seat)
                                remaining_seats.pop(remaining_seats.index(new_player_chosen_seat))
                                switch_to_next_player_flag = True # Update the flag to get next player's input
                            else:
                                # Player may not necessarily want to update their center seat - could sit at seat #1 and add only seat #2, not caring about seat #3
                                pass
                            """
    """
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
        """

    def print_all_seated_players_stats(self):
        for player in self.seated_players.values():
            if (player != None):
                player.print_player_stats()

    def start_game(self):
        print("STARTING GAME WITH THE FOLLOWING PLAYERS:")
        for table_seat, seated_player in self.seated_players.items():
            if seated_player != None:
                print(f"'{seated_player.name}' in Seat #{table_seat}")
        # Initialize natural blackjack and side bet tracking dictionaries for each unique player
        for seated_player in set(self.seated_players.values()):
            if seated_player != None:
                self.current_round_natural_blackjacks[seated_player] = []
                self.current_round_placed_side_bets_1[seated_player] = []
                self.current_round_placed_side_bets_2[seated_player] = []
        # Initialize first player (sitting leftmost w.r.t. dealer) to be active
        for seated_player in self.seated_players.values():
            if seated_player != None:
                self.active_player = seated_player
                break
        # Log last player-occupied seat before Dealer
        for seat_number, player in reversed(list(self.seated_players.items())):
            if player != None:
                self.last_occupied_seat = seat_number
                break
        # Add all new joined players to known
        for seated_player in self.seated_players.values():
            if seated_player != None:
                if seated_player not in self.known_players:
                    self.known_players.append(seated_player)
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


    # COMPACT
    def get_player_bet(self, player, seat_name, side_bet_name = None):
        if side_bet_name == None:
            min_bet = self.min_table_bet
            max_bet = self.max_table_bet
            player_side_bet_index = None
        else:
            side_bet_index = self.table_active_side_bet_names.index(side_bet_name)
            min_bet = self.table_active_side_bet_limits[side_bet_index][0]
            max_bet = self.table_active_side_bet_limits[side_bet_index][1]
            player_side_bet_index = player.placed_side_bet_names[seat_name].index(side_bet_name)
        prutils.view_chip_betting_interface()
        player.print_player_chip_pool()
        while True:
            # player_side_bet_index is None for main_bet, 0 if this is first side bet placed, 1 if this is second side bet
            if player.get_bet_input_character(min_bet, max_bet, seat_name, player_side_bet_index):
                break


    """
    def get_player_main_bet(self, player, seat_name):
        prutils.view_chip_betting_interface()
        player.print_player_chip_pool()
        while True:
            if player.get_main_bet_input_character(self.min_table_bet, self.max_table_bet, seat_name):
                print("Exiting betting interface...")
                break

    def get_player_side_bet(self, player, seat_name, side_bet_index):
        min_side_bet = self.table_active_side_bet_limits[side_bet_index][0]
        max_side_bet = self.table_active_side_bet_limits[side_bet_index][1]
        prutils.view_chip_betting_interface()
        player.print_player_chip_pool()
        while True:
            if player.get_side_bet_input_character(min_side_bet, max_side_bet, seat_name, side_bet_index):
                print("Exiting betting interface...")
                break
    """

    # UNIFY get_main_bet_input_character() and get_side_bet_input_character() INTO ONE FUNCTION


    # Check where main bet fields are initialized AND reset for next round
    # Repeat for side bets



    # Todo AB: Get main and side bet for each given seat (max of 2 non-insurance side bets as those are offered only in INITIAL_SCORING)
    def get_bets_from_all_one_player_occupied_seats(self, player):
        # Get each player's main and side bets from up to 3 seats they can occupy
        for seat_name, seat_pos in player.occupied_seats.items():
            if (seat_pos != None):
                # Get main bet for chosen seat
                player.init_main_bet_fields(seat_name)
                print(f"Player '{player.name}' is placing a main bet at Seat #{seat_pos} (their '{seat_name}')")
                self.get_player_bet(player, seat_name)
                # Get up to 2 side bets for chosen seat
                for side_bet_name in self.table_active_side_bet_names:
                    print(f"Player '{player.name}', would you like to place a side bet of '{side_bet_name}' at Seat #{seat_pos}?")
                    print("Press 'y' for Yes', 'n' for No.")
                    # Continuously prompt player for 'y' or 'n' response until they enter a valid response
                    while True:
                        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
                        match key:
                            case 'y':
                                player.init_side_bet_fields(seat_name, side_bet_name)
                                # Track side bets for each player, as they're placed
                                # USE TRACKED SIDE BETS FOR SCORING AND FUND TRANSFER
                                if side_bet_name == self.table_active_side_bet_names[0]:
                                    self.current_round_placed_side_bets_1[player].append(seat_name)
                                else:
                                    self.current_round_placed_side_bets_2[player].append(seat_name)
                                print(f"Player '{player.name}' is placing a side bet of '{side_bet_name}' at Seat #{seat_pos} (their '{seat_name}')")
                                self.get_player_bet(player, seat_name, side_bet_name)
                                break
                            case 'n':
                                print(f"Player '{player.name}' chooses not to place side bet of {side_bet_name} at Seat #{seat_pos} (their '{seat_name}')")
                                break
                            case other:
                                sys.stderr.write(f"Invalid input '{key}'\n")
                                print(f"Provide one of the following valid keys - 'y' to place a side bet of {side_bet_name}, 'n' to skip it this round.")
                print("Exiting betting interface...")




    def get_all_players_bets(self):
        for seated_player in self.seated_players.values():
            if (seated_player != None):
                self.get_bets_from_all_one_player_occupied_seats(seated_player)
                #self.active_player.print_player_stats()
        self.transition(GameState.DEALING)


    def handle_front_cut_card(self):
        if ('front_cut_card' == self.shoe[0]):
            self.discard.extend([self.shoe.pop(0)])


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
        self.print_all_hands()
        percentage_of_shoe_dealt = int(round(100-(100*(len(self.shoe)/(2+self.num_of_decks*52))), 0))
        print(f"{percentage_of_shoe_dealt}% of the shoe dealt (reshuffling at round end past {str(self.pen)}%)")
        self.transition(GameState.PRE_SCORING)


    def handle_side_bet_if_placed(self, side_bet_name):
        if side_bet_name in self.table_active_side_bet_names:
            side_bet_index = self.table_active_side_bet_names.index(side_bet_name)
            placed_side_bet_dict_name = 'current_round_placed_side_bets_' + str(side_bet_index + 1)
            placed_side_bet_dict = getattr(self, placed_side_bet_dict_name)
            for player, seat_names in placed_side_bet_dict.items():
                if seat_names != []:
                    for seat_name in seat_names:
                        print(f"Handling side bet of '{side_bet_name}' for player '{player.name}' at Seat #{player.occupied_seats[seat_name]} (their '{seat_name}')")
                        self.side_bet_handlers[side_bet_name](player, seat_name)
                else:
                    print(f"Player '{player.name}' has not placed any side bets of '{side_bet_name}'")
        else:
            if side_bet_name in self.supported_side_bet_names:
                print(f"Side bet of '{side_bet_name}' is not supported at this table")
            else:
                sys.stderr.write(f"Side bet {side_bet_name} is not supported at this Casino!\n")

    def handle_perfect_pairs_side_bet(self, player, seat_name):
        # Variables for bet check logic compactness
        first_hand_card = player.hands[seat_name][0]
        second_hand_card = player.hands[seat_name][1]
        first_hand_card_rank = first_hand_card[:-1]
        second_hand_card_rank = second_hand_card[:-1]
        first_hand_card_suit = first_hand_card[-1]
        second_hand_card_suit = second_hand_card[-1]
        if first_hand_card_suit in ['H', 'D']:
            first_hand_card_color = 'Red'
        else:
            first_hand_card_color = 'Black'
        if second_hand_card_suit in ['H', 'D']:
            second_hand_card_color = 'Red'
        else:
            second_hand_card_color = 'Black'
        # Bet value
        player_side_bet_index = player.placed_side_bet_names[seat_name].index("Perfect Pairs")
        player_side_bet_amount = player.side_bet_amounts[seat_name][player_side_bet_index]
        # Perfect Pair
        if first_hand_card == second_hand_card:
            payout = player_side_bet_amount * self.supported_side_bet_payout_tables[0]['Perfect Pair']
            self.pay_winning_player_bet(player, seat_name, "Perfect Pairs", payout)
        elif first_hand_card_rank == second_hand_card_rank:
            # Colored Pair
            if first_hand_card_color == second_hand_card_color:
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[0]['Colored Pair']
                self.pay_winning_player_bet(player, seat_name, "Perfect Pairs", payout)
            # Red/Black Pair
            else:
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[0]['Red/Black Pair']
                self.pay_winning_player_bet(player, seat_name, "Perfect Pairs", payout)
        else:
            self.collect_losing_player_bet(player, seat_name, "Perfect Pairs")

    def handle_match_the_dealer_side_bet(self, player, seat_name):
        # Variables for bet check logic compactness
        first_hand_card = player.hands[seat_name][0]
        second_hand_card = player.hands[seat_name][1]
        dealer_up_card = self.dealer.hands['center_seat'][0]
        first_hand_card_rank = first_hand_card[:-1]
        second_hand_card_rank = second_hand_card[:-1]
        dealer_up_card_rank = dealer_up_card[:-1]
        first_hand_card_suit = first_hand_card[-1]
        second_hand_card_suit = second_hand_card[-1]
        dealer_up_card_suit = dealer_up_card[-1]
        # Conditionals for bet check logic compactness
        first_hand_card_suited_match = first_hand_card == dealer_up_card
        second_hand_card_suited_match = second_hand_card == dealer_up_card
        first_hand_card_non_suited_match = (first_hand_card_rank == dealer_up_card_rank and 
                                            first_hand_card_suit != dealer_up_card_suit)
        second_hand_card_non_suited_match = (second_hand_card_rank == dealer_up_card_rank and 
                                                second_hand_card_suit != dealer_up_card_suit)
        first_hand_card_not_a_match = first_hand_card_rank != dealer_up_card_rank
        second_hand_card_not_a_match = second_hand_card_rank != dealer_up_card_rank
        # Bet value
        player_side_bet_index = player.placed_side_bet_names[seat_name].index("Match the Dealer")
        player_side_bet_amount = player.side_bet_amounts[seat_name][player_side_bet_index]
        # 2 Suited Matches
        if first_hand_card_suited_match and second_hand_card_suited_match:
            payout = player_side_bet_amount * self.supported_side_bet_payout_tables[1]['2 Suited Matches']
            self.pay_winning_player_bet(player, seat_name, "Match the Dealer", payout)
        # 1 Non-Suited & 1 Suited Match
        elif ((first_hand_card_suited_match and second_hand_card_non_suited_match) or 
                (first_hand_card_non_suited_match and second_hand_card_suited_match)):
            payout = player_side_bet_amount * self.supported_side_bet_payout_tables[1]['1 Non-Suited & 1 Suited Match']
            self.pay_winning_player_bet(player, seat_name, "Match the Dealer", payout)
        # 1 Suited Match
        elif ((first_hand_card_suited_match and second_hand_card_not_a_match) or 
                (first_hand_card_not_a_match and second_hand_card_suited_match)):
            payout = player_side_bet_amount * self.supported_side_bet_payout_tables[1]['1 Suited Match']
            self.pay_winning_player_bet(player, seat_name, "Match the Dealer", payout)
        # 2 Non-Suited Matches
        elif (first_hand_card_non_suited_match and second_hand_card_non_suited_match):
            payout = player_side_bet_amount * self.supported_side_bet_payout_tables[1]['2 Non-Suited Matches']
            self.pay_winning_player_bet(player, seat_name, "Match the Dealer", payout)
        # 1 Non-Suited Match
        elif ((first_hand_card_non_suited_match and second_hand_card_not_a_match) or 
                (first_hand_card_not_a_match and second_hand_card_non_suited_match)):
            payout = player_side_bet_amount * self.supported_side_bet_payout_tables[1]['1 Non-Suited Match']
            self.pay_winning_player_bet(player, seat_name, "Match the Dealer", payout)
        else:
            self.collect_losing_player_bet(player, seat_name, "Match the Dealer")

    def handle_lucky_ladies_side_bet(self, player, seat_name):
        # Variables for bet check logic compactness
        first_hand_card = player.hands[seat_name][0]
        second_hand_card = player.hands[seat_name][1]
        dealer_up_card = self.dealer.hands['center_seat'][0]
        first_hand_card_rank = first_hand_card[:-1]
        second_hand_card_rank = second_hand_card[:-1]
        dealer_up_card_rank = dealer_up_card[:-1]
        first_hand_card_suit = first_hand_card[-1]
        second_hand_card_suit = second_hand_card[-1]
        first_hand_card_value = bjo.cards[first_hand_card_rank][-1]
        if first_hand_card_rank == 'A' and second_hand_card_rank == 'A':
            second_hand_card_value = bjo.cards[first_hand_card_rank][0]
        else:
            second_hand_card_value = bjo.cards[first_hand_card_rank][-1]
        # Bet value
        player_side_bet_index = player.placed_side_bet_names[seat_name].index("Lucky Ladies")
        player_side_bet_amount = player.side_bet_amounts[seat_name][player_side_bet_index]
        if self.state == GameState.PRE_SCORING:
            if dealer_up_card_rank not in ['10', 'J', 'Q', 'K', 'A']:
                # Handle non-Blackjack 'Queen of Hearts Pair' payout
                if (first_hand_card == second_hand_card == 'QH'):
                    payout = player_side_bet_amount * self.supported_side_bet_payout_tables[2]['Queen of Hearts Pair']
                    self.pay_winning_player_bet(player, seat_name, "Lucky Ladies", payout)
            # Handle payouts independent of dealer_up_card
            elif ((first_hand_card == second_hand_card != 'QH') and (first_hand_card_value == second_hand_card_value == 10)):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[2]['Matched 20']
                self.pay_winning_player_bet(player, seat_name, "Lucky Ladies", payout)
            elif ((first_hand_card_suit == second_hand_card_suit) and (first_hand_card_value + second_hand_card_value == 20)):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[2]['Suited 20']
                self.pay_winning_player_bet(player, seat_name, "Lucky Ladies", payout)
            elif ((first_hand_card_suit != second_hand_card_suit) and (first_hand_card_value + second_hand_card_value == 20)):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[2]['Unsuited 20']
                self.pay_winning_player_bet(player, seat_name, "Lucky Ladies", payout)
            else:
                self.collect_losing_player_bet(player, seat_name, "Lucky Ladies")
        # Handle all 'Queen of Hearts Pair' payouts after checking for Dealer Blackjack
        elif (self.state == GameState.INITIAL_SCORING) and (first_hand_card == second_hand_card == 'QH'):
            if self.dealer.hand_scores['center_seat'] == 21:
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[2]['Queen of Hearts Pair (with Dealer Blackjack)']
                self.pay_winning_player_bet(player, seat_name, "Lucky Ladies", payout)
            else:
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[2]['Queen of Hearts Pair']
                self.pay_winning_player_bet(player, seat_name, "Lucky Ladies", payout)
        else:
            sys.stderr.write(f"Lucky ladies handler called from an unsupported state {self.state}\n")

    def handle_kings_bounty_side_bet(self, player, seat_name):
        # Variables for bet check logic compactness
        first_hand_card = player.hands[seat_name][0]
        second_hand_card = player.hands[seat_name][1]
        dealer_up_card = self.dealer.hands['center_seat'][0]
        first_hand_card_rank = first_hand_card[:-1]
        second_hand_card_rank = second_hand_card[:-1]
        dealer_up_card_rank = dealer_up_card[:-1]
        first_hand_card_suit = first_hand_card[-1]
        second_hand_card_suit = second_hand_card[-1]
        first_hand_card_value = bjo.cards[first_hand_card_rank][-1]
        if first_hand_card_rank == 'A' and second_hand_card_rank == 'A':
            second_hand_card_value = bjo.cards[first_hand_card_rank][0]
        else:
            second_hand_card_value = bjo.cards[first_hand_card_rank][-1]
        # Bet value
        player_side_bet_index = player.placed_side_bet_names[seat_name].index("King's Bounty")
        player_side_bet_amount = player.side_bet_amounts[seat_name][player_side_bet_index]
        if self.state == GameState.PRE_SCORING:
            if dealer_up_card_rank not in ['10', 'J', 'Q', 'K', 'A']:
                # Handle non-Blackjack 'King of Spades Pair' payout
                if (first_hand_card == second_hand_card == 'KS'):
                    payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['King of Spades Pair']
                    self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            # Handle payouts independent of dealer_up_card
            elif ((first_hand_card_suit == second_hand_card_suit != 'S') and (first_hand_card_rank == second_hand_card_rank == 'K')):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['Suited Kings Pair (not spades)']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            elif ((first_hand_card_suit == second_hand_card_suit) 
                  and (first_hand_card_value == second_hand_card_value == 10) 
                  and (first_hand_card_rank == second_hand_card_rank != 'K')):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['Suited Qs, Js, or 10s Pair']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            elif ((first_hand_card_suit == second_hand_card_suit) and (first_hand_card_value + second_hand_card_value == 20)):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['Suited 20']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            elif ((first_hand_card_suit != second_hand_card_suit) and (first_hand_card_rank == second_hand_card_rank == 'K')):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['Unsuited Kings Pair']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            elif ((first_hand_card_suit != second_hand_card_suit) and (first_hand_card_value + second_hand_card_value == 20)):
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['Unsuited 20']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            else:
                self.collect_losing_player_bet(player, seat_name, "King's Bounty")
        # Handle all 'King of Spades Pair' payouts after checking for Dealer Blackjack
        elif (self.state == GameState.INITIAL_SCORING) and (first_hand_card == second_hand_card == 'KS'):
            if self.dealer.hand_scores['center_seat'] == 21:
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['King of Spades Pair (with Dealer Blackjack)']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
            else:
                payout = player_side_bet_amount * self.supported_side_bet_payout_tables[3]['King of Spades Pair']
                self.pay_winning_player_bet(player, seat_name, "King's Bounty", payout)
        else:
            sys.stderr.write(f"Lucky ladies handler called from an unsupported state {self.state}\n")

    def handle_buster_blackjack_side_bet(self, player, seat_name):
        # Todo AB: Implement Buster Blackjack side bet handling
        pass

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
                            self.current_round_natural_blackjacks[player].append(seat_name)
        #self.print_all_players_with_natural_blackjack_hands()
        dealer_hand_score = bjl.highest_hand_score(self.dealer.hands['center_seat'])
        self.dealer.hand_scores['center_seat'] = dealer_hand_score


    def get_player_surrender_response(self, player, seat_name):
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'y':
                print(f"Player '{player.name}' surrenders hand {player.hands[seat_name]}")
                ## Collect player's bet from seat_name ##
                player_chip_bet = player.main_bets[seat_name]
                for chip_color, chip_count in player_chip_bet.items():
                    # Move all bet chips from Player's betting circle to Dealer and update Dealer's balance
                    chip_value = bjo.chips[chip_color]
                    player_chip_bet[chip_color] -= chip_count
                    self.dealer.chips[chip_color] += chip_count
                    self.dealer.chip_pool_balance += chip_count*chip_value
                # Refund Player half of their bet amount rounded down, placing it in the betting circle
                


                self.dealer.cast_whole_number_chip_pool_balance_to_int()
                ## Reset losing player's bet ##
                getattr(player, bets_name)[seat_name] = None # player.main_bets[seat_name] OR player.side_bets[seat_name]
                bet_amounts_name = bet_type + '_bet_amounts'
                getattr(player, bet_amounts_name)[seat_name] = None # player.main_bet_amounts[seat_name] OR player.side_bet_amounts[seat_name]
                # No need to subtract chips and chip_pool_balance for Player - already done when a bet is submitted
                





                # Return half of player's bet (rounded down) back to the betting circle at seat_name
                # Collect player hand at seat_name and reset score --> WRITE A FUNCTION TO HANDLE THIS RECURRING PROCEDURE
                pass
            case 'n':
                pass
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide one of the following valid keys - 'y' for Yes to early surrender, 'n' for No to early surrender.")

    def offer_early_surrender_if_used_at_table_to_all_players(self): # Todo AB: Test offer_early_surrender_if_used_at_table_to_all_players()
        dealer_up_card = self.dealer.hands['center_seat'][0]
        dealer_up_card_rank = dealer_up_card[:-1]
        if ((self.surrender_rule == 'ES') or ((self.surrender_rule == 'ES10') and (dealer_up_card_rank in ['10', 'J', 'Q', 'K']))):
            for player in self.seated_players.values():
                if player != None:
                    for seat_name, seat_number in player.occupied_seats.items():
                        if seat_number != None:
                            print(f"Player '{player.name}', would you like to make an early surrender of hand {player.hands[seat_name]} at Seat ", end='')
                            print(f"#{player.occupied_seats[seat_name]} and forfeit half of your bet of ${player.main_bet_amounts[seat_name]} (rounded up)?")
                            print("Press 'y' for Yes', 'n' for No.")
                            self.get_player_surrender_response(player, seat_name)
        else:
            print(f"Early surrender isn't used at the table - table's surrender rule is '{self.surrender_rule}'")
        self.transition(GameState.INITIAL_SCORING)


    def offer_even_money_and_insurance_side_bet(self):
        pass


    def offer_late_surrender_if_used_at_table(self):
        if self.surrender_rule == 'LS':
            pass

    def reveal_dealer_hand(self):
        print(f"Dealer hand is {self.dealer.hands['center_seat']}")


    def reset_natural_blackjack_tracking(self): # Removes all natural player blackjacks from being tracked this round
        for player in self.current_round_natural_blackjacks.keys():
            #print(f"Dealer pushes against player {player.name} with natural blackjack of {hand})
            self.current_round_natural_blackjacks[player].clear()

    def collect_losing_player_bet(self, player, seat_name, side_bet_name = None):
        if seat_name not in ['right_seat', 'center_seat', 'left_seat']:
            sys.stderr.write(f"Invalid seat_name '{seat_name}' provided! Valid seat names are 'right_seat', 'center_seat', and 'left_seat'")     
        # Retrieve a losing bet dictionary
        if side_bet_name == None:
            player_chip_bet = getattr(player, 'main_bets')[seat_name] # player.main_bets[seat_name]
        elif side_bet_name in self.supported_side_bet_names:
            player_side_bet_index = player.placed_side_bet_names[seat_name].index(side_bet_name)
            player_chip_bet = getattr(player, 'side_bets')[seat_name][player_side_bet_index] # player.side_bets[seat_name][0] or player.side_bets[seat_name][1] 
        else:
            sys.stderr.write(f"Unsupported side bet name '{side_bet_name}' provided! Valid side bet names - {self.supported_side_bet_names}")
        if player_chip_bet != None:
            # Transfer chips from a losing bet dictionary to dealer chip pool; update dealer chip balance
            for chip_color, chip_count in player_chip_bet.items():
                chip_value = bjo.chips[chip_color]
                self.dealer.chips[chip_color] += chip_count
                self.dealer.chip_pool_balance += chip_count*chip_value # No need to subtract chips and chip_pool_balance for Player - happened when bet was submitted
            self.dealer.cast_whole_number_chip_pool_balance_to_int()
            # Reset player's losing bet dictionary and discard hand
            if side_bet_name == None:
                getattr(player, 'main_bets')[seat_name] = None # player.main_bets[seat_name]
                getattr(player, 'main_bet_amounts')[seat_name] = None # player.main_bet_amounts[seat_name]
            elif side_bet_name in self.supported_side_bet_names:
                player_side_bet_index = player.placed_side_bet_names[seat_name].index(side_bet_name)
                getattr(player, 'side_bets')[seat_name][player_side_bet_index] = None # player.side_bets[seat_name][1] or player.side_bets[seat_name][2]
                getattr(player, 'side_bet_amounts')[seat_name][player_side_bet_index] = None # player.side_bet_amounts[seat_name][1] or player.side_bet_amounts[seat_name][2]
            else:
                sys.stderr.write(f"Unsupported side bet name '{side_bet_name}' provided! Valid side bet names - {self.supported_side_bet_names}")
            self.discard.extend(player.hands[seat_name])
        else:
            sys.stderr.write(f"Player chip bet is 'None'! Chip transfer from player '{player.name}' to Dealer cannot be completed.")

    def collect_losing_main_bets(self):
        # Go through main bet hands left-to-right from dealer's POV and collect losing main bets
        # Note: Player model is structured in order from rightmost to leftmost player hand, allowing to simply iterate over occupied_seats
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        print(f"Player '{player.name}' loses with hand of {player.hands[seat_name]} to Dealer's Blackjack of {self.dealer.hands['center_seat']}")
                        self.collect_losing_player_bet(player, seat_name)

    def collect_losing_side_bets(self, side_bet_index):
        # Go through side bet hands left-to-right from dealer's POV and collect losing side bets
        # Note: Player model is structured in order from rightmost to leftmost player hand, allowing to simply iterate over occupied_seats
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        print(f"Player '{player.name}' loses side bet of hand {player.hands[seat_name]} to Dealer")
                        self.collect_losing_player_bet(player, seat_name, 'side', side_bet_index)


    # Chip transfer functions
    # Examples:
    # src_dict = dealer.chips // dst_dict = player.main_bet_winnings[seat_name]
    # // Update dealer.chip_pool_balance AND player.main_bet_winnings_amounts[seat_name]
    # src_dict = dealer.chips // dst_dict = player.side_bet_winnings[seat_name][side_bet_index]
    # // Update 
    # src_dict = player.main_bets[seat_name] // dst_dict = dealer.chips
    # // Update 
    # src_dict = player.side_bets[seat_name] // dst_dict = dealer.chips
    # // Update 
    # Todo AB: Test transfer_chips_from_dealer_to_player()
    
    def pay_winning_player_bet(self, player, seat_name, side_bet_name, payout):
        if seat_name not in ['right_seat', 'center_seat', 'left_seat']:
            sys.stderr.write(f"Invalid seat_name '{seat_name}' provided! Valid seat names are 'right_seat', 'center_seat', and 'left_seat'")
        # 1. Retrieve all fields involved in chip transfer
        if side_bet_name == None:
            # For main bets
            player_chip_bet = getattr(player, 'main_bets')[seat_name] # player.main_bets[seat_name]
            player_chip_winnings = getattr(player, 'main_bet_winnings')[seat_name] # player.main_bet_winnings[seat_name]
            player_bet_amount = getattr(player, 'main_bet_amounts')[seat_name] # player.main_bet_amounts[seat_name]
            player_winnings_amount = getattr(player, 'main_bet_winnings_amounts')[seat_name] # player.main_bet_winnings_amounts[seat_name]
        elif side_bet_name in self.supported_side_bet_names:
            # For side bets
            player_side_bet_index = player.placed_side_bet_names[seat_name].index(side_bet_name)
            player_chip_bet = getattr(player, 'side_bets')[seat_name][player_side_bet_index] # player.side_bets[seat_name][0] or player.side_bets[seat_name][1]
            player_chip_winnings = getattr(player, 'side_bet_winnings')[seat_name][player_side_bet_index] # player.side_bet_winnings[seat_name][0] or player.side_bet_winnings[seat_name][1]
            player_bet_amount = getattr(player, 'side_bet_amounts')[seat_name][player_side_bet_index] # player.side_bet_amounts[seat_name][0] or player.side_bet_amounts[seat_name][1]
            player_winnings_amount = getattr(player, 'side_bet_winnings_amounts')[seat_name][player_side_bet_index] # player.side_bet_winnings_amounts[seat_name][0] or player.side_bet_winnings_amounts[seat_name][1]
        else:
            sys.stderr.write(f"Unsupported side bet name '{side_bet_name}' provided! Valid side bet names - {self.supported_side_bet_names}")
        # 2. Check that transfer can be completed - no involved player fields are set to None
        if None in [player_chip_bet, player_chip_winnings, player_bet_amount, player_winnings_amount]:
            sys.stderr.write(f"Chip transfer couldn't be completed - one of the used transfer fields is set to None\n")
            sys.stderr.write(f"player_chip_bet --> {player_chip_bet}\n")
            sys.stderr.write(f"player_chip_winnings --> {player_chip_winnings}\n")
            sys.stderr.write(f"player_bet_amount --> {player_bet_amount}\n")
            sys.stderr.write(f"player_winnings_amount --> {player_winnings_amount}\n")
            return
        # 3. Special Case for 3:2 Blackjack /w $1 bet - Swap $1 chip in betting circle /w a Pink chip
        if (payout == 1.5):
            player_chip_bet['White'] -= 1
            self.dealer.chips['White'] += 1
            self.dealer.chip_pool_balance += 1
            self.dealer.chips['Pink'] -= 1
            self.dealer.chip_pool_balance -= 2.5
            self.dealer.cast_whole_number_chip_pool_balance_to_int() # Turns balances such as 37.5 - 2.5 = 35.0 to 35 w/o decimal
            player_chip_bet['Pink'] += 1
            player_winnings_amount = 1.5
            return
        # 4. Pay a Pink chip for a fractional bet (multiple of 0.5)
        if (type(payout) == float and (payout % 0.5 == 0)):
            self.dealer.chips['Pink'] -= 1
            self.dealer.chip_pool_balance -= 2.5
            self.dealer.cast_whole_number_chip_pool_balance_to_int() # Turns balances such as 37.5 - 2.5 = 35.0 to 35 w/o decimal
            player_chip_winnings['Pink'] += 1
            player_winnings_amount += 2.5
            print(f"Paying a Pink chip for payout of ${payout}")
            payout -= 2.5
        # 5. Pay remaining part of winnings, if any
        if (payout != 0):
            print(f"Remaining payout is ${payout}")
            for chip_name, chip_value in bjo.reverse_chips.items():
                if chip_name != 'Pink':
                    remainder = payout % chip_value
                    if (remainder in range(0, payout)): # range() excludes upper bound in generated list
                        chip_count = math.floor(payout/chip_value)
                        self.dealer.chips[chip_name] -= chip_count
                        self.dealer.chip_pool_balance -= chip_count*chip_value
                        self.dealer.cast_whole_number_chip_pool_balance_to_int() # Turns balances such as 37.5 - 2.5 = 35.0 to 35 w/o decimal
                        player_chip_winnings[chip_name] += chip_count
                        player_winnings_amount += chip_count*chip_value
                        print(f"Paying {chip_count} {chip_name} chips for remaining payout of ${payout}")
                        payout -= chip_count*chip_value
                        print(f"${payout} remaining to be paid out")
                        if (payout == 0):
                            player.cast_whole_number_bet_winnings_amount_to_int()
                            break

    """
    player.cast_whole_number_chip_pool_balance_to_int() # Turns balances such as 37.5 + 2.5 = 40.0 to 40 w/o decimal
    """



    # Todo AB: fix pay_winning_main_bets() to be functional and unit-test it
    def pays_winning_main_bets(self):
        # Go through main bet hands left-to-right from dealer's POV and pay winning main bets
        if self.state == GameState.INITIAL_SCORING:
            #players_with_blackjacks = [player for player in self.current_round_natural_blackjacks.keys()]
            #print("Players /w Blackjack hands are:", players_with_blackjacks[0].name)
            for player in self.current_round_natural_blackjacks.keys():
                player_blackjack_seat_names = self.current_round_natural_blackjacks[player]
                for seat_name in player_blackjack_seat_names:
                    
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


    # Helper methods for Blackjack state machine
    def discard_hand_and_reset_score(self, player, seat_name):
        if seat_name not in ['right_seat', 'center_seat', 'left_seat']:
            self.discard.extend(player.hands[seat_name])
            player.hands[seat_name].clear()
            player.hand_scores[seat_name] = 0
        else:
            sys.stderr.write(f"Invalid seat_name '{seat_name}' provided! Valid seat names are 'right_seat', 'center_seat', and 'left_seat'")

    def discard_all_hands_in_play_and_reset_all_hand_scores(self):
        for player in self.seated_players.values():
            if player != None:
                for seat_name, seat_number in player.occupied_seats.items():
                    if seat_number != None:
                        self.discard_hand_and_reset_score(player, seat_name)
        self.discard_hand_and_reset_score(self.dealer, 'center_seat')

    def handle_round_end_transition(self):
        if 'front_cut_card' in self.discard:
            print("SHOE END, reshuffling!")
            self.transition(GameState.SHUFFLING)
        else:
            self.transition(GameState.BETTING)

    def handle_dealer_blackjack(self):
        # Collect all losing blackjack bets right-to-left
        for seat_number, player in reversed(list(self.seated_players.items())):
            if player != None:
                seat_index = list(player.occupied_seats.values()).index(seat_number)
                seat_name = list(player.occupied_seats.keys())[seat_index]
                if player.hand_scores[seat_name] < 21:
                    self.collect_losing_player_bet(player, seat_name)
        # Collect all player hands right-to-left
        for seat_number, player in reversed(list(self.seated_players.items())):
            if player != None:
                seat_index = list(player.occupied_seats.values()).index(seat_number)
                seat_name = list(player.occupied_seats.keys())[seat_index]
                self.discard_hand_and_reset_score(player, seat_name)
        self.discard_hand_and_reset_score(self.dealer, 'center_seat')
        print("ROUND END")
        self.transition(GameState.BETTING)


    def play_all_remaining_players_hands(self):
        for player in self.seated_players.values():
            if (player != None):
                for seat_name, seat_number in player.occupied_seats.items():
                    if (seat_number != None):
                        print(f"Player '{player.name}' is choosing an action at Seat #{seat_number} (their '{seat_name}')")
                        prutils.view_player_turn_action_options()
                        while True:
                            # Loop over until player chooses to stand or busts
                            if self.play_player_hand(player, seat_name, seat_number):
                                # Transition to DEALER_PLAYING if played hand is last before Dealer
                                if seat_number == self.last_occupied_seat:
                                    self.transition(GameState.DEALER_PLAYING)
                                print("Finished playing a hand, passing...")
                                break

    def play_player_hand(self, player, seat_name, seat_number):
        # Todo AB: Make sure the above code scales with player making multiple hand bets
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case '1':
                print(f"Executing action 'stand' for player '{player.name}' at Seat #{seat_number} (their '{seat_name}')")
                return True # alternatively self.stand(player) returning True
            case '2':
                print(f"Executing action 'hit' for player '{player.name}' at Seat #{seat_number} (their '{seat_name}')")
                self.hit(player, seat_name)
            case '3':
                print(f"Executing action 'double' for player '{player.name}' at Seat #{seat_number} (their '{seat_name}')")
                self.double(player, seat_name)
            case '4':
                print(f"Executing action 'split' for player '{player.name}' at Seat #{seat_number} (their '{seat_name}')")
                self.split(player, seat_name)
            case '5':
                print(f"Executing action 'surrender' for player '{player.name}' at Seat #{seat_number} (their '{seat_name}')")
                self.surrender(player, seat_name)
            case 'v':
                prutils.view_player_turn_action_options()
            case 'p':
                player.print_current_bet(seat_name, None)
                #player.print_current_main_bet(seat_name)
            case 'c':
                self.color_up(player) # Todo AB: implement color_up()
            case 'b':
                self.break_down(player) # Todo AB: implement break_down()
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide a valid key or press 'v' to see valid key input options")


    def dealer_plays(self):
        initial_dealer_hand_score = self.dealer.hand_scores['center_seat']
        if self.seventeen_rule == 'S17':
            print(f"{self.seventeen_rule} rule is in play")
            if (initial_dealer_hand_score >= 17):
                print(f"Dealer stands with a score of {initial_dealer_hand_score}")
                self.transition(GameState.FINAL_SCORING)
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
            self.transition(GameState.FINAL_SCORING)
        elif self.seventeen_rule == 'H17':
            print(f"{self.seventeen_rule} rule is in play")
            if (initial_dealer_hand_score > 17):
                print(f"Dealer stands with a score of {initial_dealer_hand_score}")
                self.transition(GameState.FINAL_SCORING)
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
                self.transition(GameState.FINAL_SCORING)
        # debug log and assert
        else:
            sys.stderr.write("[ERROR] Seventeen rule syntax not recognized\n")


    """
    def check_for_and_handle_initial_players_blackjacks_if_any_present(self):
        if (len(self.current_round_natural_blackjacks.keys()) == 0):
            print("No players have natural Blackjack.")
            self.transition(GameState.PLAYERS_PLAYING)
        else:
            print("Paying Blackjacks to each eligible player hand")
            self.reveal_dealer_hand()
            self.pay_winning_main_bets()
            #self.reset_natural_blackjack_tracking()


            
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
    """

    def handle_players_blackjacks(self):
        # Pay all winning blackjack bets right-to-left
        for player, seat_name_list in self.current_round_natural_blackjacks.keys():
            for seat_name in reversed(seat_name_list):
                payout = player.main_bet_amounts[seat_name] * self.blackjack_ratio
                if self.blackjack_ratio == 1.2: # Rounding only applies to 6:5 Blackjack payout ratio
                    payout = round(payout)
                    print(f"Paying Blackjack 6:5 of ${payout} to player {player.name} with hand of {player.hands[seat_name]}")
                else:
                    print(f"Paying Blackjack 3:2 of ${payout} to player {player.name} with hand of {player.hands[seat_name]}")
                self.pay_winning_player_bet(player, seat_name, None, payout)
        # Collect winning blackjack player hands right-to-left
        for player, seat_name_list in self.current_round_natural_blackjacks.keys():
            for seat_name in reversed(seat_name_list):
                self.discard_hand_and_reset_score(player, seat_name)

    """
    def get_game_option_input_character(self):
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                self.view_game_launch_options()
            case 'd':
                self.print_player_chip_pool()
            case 'p':
                self.print_current_bet(seat_name)
            case 'r':
                self.reset_current_bet(seat)
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide a valid key or press 'v' to see valid key input options")
    """

    def step(self):
        print(f"Current state: {self.state}")
        match self.state:
            case GameState.WAITING:
                self.wait_for_players_to_join()
            case GameState.STARTING:
                #self.print_all_seated_players_stats()
                self.start_game()
            case GameState.SHUFFLING:
                self.shuffle_cut_and_burn(None) # Todo AB: pen % is different upon each reshuffle in a single session, need it fixed?
            case GameState.BETTING:
                self.get_all_players_bets() # Todo AB: update get_all_players_bets() to work /w players occupying multiple seats
            case GameState.DEALING:
                self.deal() # Todo AB: Update deal() to work with players occupying multiple seats
            case GameState.PRE_SCORING:
                #print(f"Placed {self.table_active_side_bet_names[0]} side bets:\n{self.current_round_placed_side_bets_1}")
                #print(f"Placed {self.table_active_side_bet_names[1]} side bets:\n{self.current_round_placed_side_bets_2}")
                for side_bet_name in ["Perfect Pairs", "Match the Dealer", "Lucky Ladies", "King's Bounty"]:
                    #print(f"Checking for placed '{side_bet_name}' side bets")
                    self.handle_side_bet_if_placed(side_bet_name)
                self.transition(GameState.INITIAL_SCORING)
            case GameState.INITIAL_SCORING:
                self.score_all_hands_in_play()
                self.offer_early_surrender_if_used_at_table_to_all_players()
                if self.current_round_remaining_player_hands != 0:
                    dealer_up_card_rank = self.dealer.hands['center_seat'][0][:-1]
                    if dealer_up_card_rank == 'A':
                        print("Dealer's face card is an Ace!")
                        print("Offering 'insurance' side bet and 'even money':")
                        self.offer_even_money_and_insurance_side_bet()
                    elif dealer_up_card_rank == '10':
                        print("Dealer's face card is a ten!")
                    if (self.dealer.hand_scores['center_seat'] == 21):
                        print(f"Dealer checks hole card, has Blackjack of {self.dealer.hands['center_seat']}!")
                        self.reveal_dealer_hand()
                        self.handle_side_bet_if_placed("Lucky Ladies")
                        self.handle_side_bet_if_placed("King's Bounty")
                        self.handle_dealer_blackjack()
                        self.handle_round_end_transition()
                    else:
                        print("Dealer can't have Blackjack.")
                        self.handle_side_bet_if_placed("Lucky Ladies")
                        self.handle_side_bet_if_placed("King's Bounty")
                        self.handle_players_blackjacks()
                        self.offer_late_surrender_if_used_at_table_to_all_players()
                        if self.current_round_remaining_player_hands == 0:
                            self.discard_hand_and_reset_score(self.dealer, 'center_seat')
                            self.handle_round_end_transition()
            case GameState.PLAYERS_PLAYING:
                self.play_all_remaining_players_hands() # if player gets blackjack, don't pay out yet (push is possible)
            case GameState.DEALER_PLAYING:
                self.dealer_plays()
                # Dealer busts --> self.handle_side_bet_if_placed("Buster Blackjack")
            case GameState.FINAL_SCORING:
                if (self.dealer.hand_scores['center_seat'] == 21):
                    self.handle_dealer_blackjack()
                else:
                    # Pay winning hands
                    # Push
                    # Collect losing hands
                    pass
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