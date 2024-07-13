""" 
File: blackjack_players.py
Author: Alexander Bulanov
"""

# Global Imports #
import msvcrt
import sys

# Local Imports #
from . import blackjack_game_objects as bjo
from . import print_utils as prutils

### Defining Players for Tracking ###
class Player:
    def __init__(self):
        self.name = None
        self.is_dealer = False
        self.cash_balance = None
        self.chips = dict.fromkeys(bjo.chip_names, 0)
        self.chip_pool_balance = 0
        self.hole_card_face_down = False
        self.occupied_seats = {
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        self.main_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        self.main_bet_amounts = { # each bet amount is stored as an integer (betting of $2.5 chips is restricted to pairs only)
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        self.main_bet_winnings = { # each set of winnings is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        self.main_bet_winnings_amounts = { # each set of winnings has dollar value stored as an integer or a float
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        self.placed_side_bet_names = { # each group of names is stored in a list in format of ['Perfect Pairs', 'Lucky Ladies', etc.]
            'right_seat': [], # side_bet_names keeps track of which group of chips in side_bets is tied to which bet
            'center_seat': [], # Side bet options - 'Perfect Pairs', 'Match the Dealer', 'Lucky Ladies', 'King's Bounty', 'Buster Blackjack', '21+3'
            'left_seat': []
        }
        self.side_bets = { # each bet is stored as a list of dictionaries in format of chip_color: chip_count
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        self.side_bet_amounts = { # each bet amount is stored as a list of integers (betting of $2.5 chips is restricted to pairs only) - [2, 10, 20]
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        self.side_bet_winnings = { # each set of winnings is stored as list of dictionaries in format of chip_color: chip_count
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        self.side_bet_winnings_amounts = { # each set of winnings is stored as a list of integers or floats, as appropriate - [3, 15, 30]
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        self.hands = { # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        self.hand_scores = {
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        self.action = None

    # Player actions are:
        # Out-of-Round:
            # Join ('j')
            # Leave ('l')
        # In-Round (Main Bets):
            # Bet ('b')
            # Stand ('st')
            # Hit ('h')
            # Double-Down ('d')
            # Split ('sp')
            # Surrender ('su')
        # In-Round (Side Bets):
            # Insurance ('i')
            # Even Money ('em')

    def create_casino_dealer():
        Dealer = Player()
        Dealer.name = 'Dealer'
        Dealer.is_dealer = True
        Dealer.cash_balance = 10000
        Dealer.chips = dict.fromkeys(bjo.chip_names, 1000)
        Dealer.chip_pool_balance = 1000*(1+2.5+5+10+25+100+500+1000+5000) # $6,643,500.00
        Dealer.hole_card_face_down = True
        Dealer.occupied_seats = {
            'right_seat': None,
            'center_seat': 8,
            'left_seat': None
        }
        Dealer.main_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        Dealer.main_bet_amounts = { # each bet amount is stored as an integer (betting of $2.5 chips is restricted to pairs only)
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        Dealer.main_bet_winnings = { # each set of winnings is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        Dealer.main_bet_winnings_amounts = { # each set of winnings has dollar value stored as an integer or a float
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        Dealer.placed_side_bet_names = { # each group of names is stored in a list in format of ['Perfect Pairs', 'Lucky Ladies', etc.]
            'right_seat': [], # side_bet_names keeps track of which group of chips in side_bets is tied to which bet
            'center_seat': [], # Side bet options - 'Perfect Pairs', 'Match the Dealer', 'Lucky Ladies', 'King's Bounty', 'Buster Blackjack', '21+3'
            'left_seat': []
        }
        Dealer.side_bets = { # each bet is stored as a list of dictionaries in format of chip_color: chip_count
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        Dealer.side_bet_amounts = { # each bet amount is stored as a list of integers (betting of $2.5 chips is restricted to pairs only) - [2, 10, 20]
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        Dealer.side_bet_winnings = { # each set of winnings is stored as list of dictionaries in format of chip_color: chip_count
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        Dealer.side_bet_winnings_amounts = { # each set of winnings is stored as a list of integers or floats, as appropriate - [3, 15, 30]
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        Dealer.hands = { # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        Dealer.hand_scores = {
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        Dealer.action = None
        return Dealer
    
    def create_new_player_from_template(player_username, preferred_seat):
        NewPlayer = Player()
        NewPlayer.name = player_username
        NewPlayer.is_dealer = False
        NewPlayer.cash_balance = 100
        NewPlayer.chips = dict.fromkeys(bjo.chip_names, 0)
        NewPlayer.chips['White'] = 50
        NewPlayer.chips['Pink'] = 30
        NewPlayer.chips['Red'] = 20
        NewPlayer.chips['Blue'] = 15
        NewPlayer.chips['Green'] = 5
        NewPlayer.chip_pool_balance = int(50*1 + 30*2.5 + 20*5 + 15*10 + 5*25)
        NewPlayer.hole_card_face_down = False
        NewPlayer.occupied_seats = {
            'right_seat': None,
            'center_seat': preferred_seat,
            'left_seat': None
        }
        NewPlayer.main_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        NewPlayer.main_bet_amounts = { # each bet amount is stored as an integer (betting of $2.5 chips is restricted to pairs only)
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        NewPlayer.main_bet_winnings = { # each set of winnings is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        NewPlayer.main_bet_winnings_amounts = { # each set of winnings has dollar value stored as an integer or a float
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        NewPlayer.placed_side_bet_names = { # each group of names is stored in a list in format of ['Perfect Pairs', 'Lucky Ladies', etc.]
            'right_seat': [], # side_bet_names keeps track of which group of chips in side_bets is tied to which bet
            'center_seat': [], # Side bet options - 'Perfect Pairs', 'Match the Dealer', 'Lucky Ladies', 'King's Bounty', 'Buster Blackjack', '21+3'
            'left_seat': []
        }
        NewPlayer.side_bets = { # each bet is stored as a list of dictionaries in format of chip_color: chip_count
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        NewPlayer.side_bet_amounts = { # each bet amount is stored as a list of integers (betting of $2.5 chips is restricted to pairs only) - [2, 10, 20]
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        NewPlayer.side_bet_winnings = { # each set of winnings is stored as list of dictionaries in format of chip_color: chip_count
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        NewPlayer.side_bet_winnings_amounts = { # each set of winnings is stored as a list of integers or floats, as appropriate - [3, 15, 30]
            'right_seat': [],
            'center_seat': [],
            'left_seat': [],
        }
        NewPlayer.hands = { # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        NewPlayer.hand_scores = {
            'right_seat': None,
            'center_seat': None,
            'left_seat': None
        }
        NewPlayer.action = None
        return NewPlayer
    
    def player_has_no_main_bets_in_play(self):
        return_bool = True
        for main_bet in self.main_bets.values(): # side bets can't exist w/o main bets already in place - no need to check them
            if main_bet != None:
                return_bool = False
                break
        return return_bool
    
    def player_has_no_side_bets_in_play(self):
        return_bool = True
        for side_bet in self.side_bets.values(): # side bets can't exist w/o main bets already in place - no need to check them
            if side_bet != None:
                return_bool = False
                break
        return return_bool

    def player_has_no_cards_in_play(self):
        return_bool = True
        for hand in self.hands.values():
            if hand != None:
                return_bool = False
                break
        return return_bool

    # Player print methods
    def print_player_stats(self, flag=None):
        print("*  *  *  *  *")
        if self.name == 'Dealer':
            print("Printing Dealer Statistics")
        else:
            print(f"Printing Statistics for Player '{self.name}'")
        for key, value in self.__dict__.items():
            match key:
                case 'name' | 'is_dealer' | 'hole_card_face_down':
                    if (flag == 'v'):
                        print(f"{key}: {value}")
                case 'cash_balance' | 'chip_pool_balance':
                    print(f"{key}: ${value}")
                case 'chips':
                    if (flag == 'v'):
                        print(f"{key}: {value}")
                    else:
                        non_zero_chips = {}
                        for chip_color, chip_count in self.chips.items():
                            if (chip_count != 0):
                                non_zero_chips[chip_color] = chip_count
                        print(f"{key}: {non_zero_chips}")
                case 'occupied_seats':
                    print(f"{key}:", end='')
                    for seat, seat_number in self.occupied_seats.items():
                        if (seat_number != None):
                            print("\n    ", end='')
                            print(f"'{seat}': #{seat_number}", end='')
                        elif (flag == 'v'):
                            print("\n    ", end='')
                            print(f"'{seat}': {seat_number}", end='')
                    print("")
                case 'main_bets' | 'side_bets':
                    print(f"{key}:", end='')
                    bet_type = getattr(self, key) # player.main_bets or player.side_bets
                    for seat, seat_number in self.occupied_seats.items():
                        if (flag == 'v'):
                            if key == 'side_bets':
                                
                                # FILL THIS IN
                                # CHECK FOR SIDE BET HERE

                                pass
                            else:
                                print(f"\n    '{seat}': {bet_type[seat]}", end='')
                        elif ((key == 'main_bets') and (self.player_has_no_main_bets_in_play())):
                            print(" None", end='')
                            break
                        elif ((key == 'side_bets') and (self.player_has_no_side_bets_in_play())):
                            print(" None", end='')
                            break
                        else:
                            if ((seat_number != None) and (bet_type[seat] != None)):
                                non_zero_bet_chips = {}
                                # CHECK FOR SIDE BET HERE
                                if key == 'side_bets':
                                    pass
                                elif key == 'main_bets':
                                    for chip_color, chip_count in bet_type[seat].items():
                                        if (chip_count != 0):
                                            non_zero_bet_chips[chip_color] = chip_count
                                print(f"\n    '{seat}': {non_zero_bet_chips}", end='')
                    print("")
                case 'main_bet_amounts' | 'side_bet_amounts':
                    print(f"{key}:", end='')
                    bet_type_amount = getattr(self, key) # player.main_bet_amounts or player.side_bet_amounts
                    for seat, seat_number in self.occupied_seats.items():
                        if (flag == 'v'):
                            if (bet_type_amount[seat] != None):
                                print(f"\n    '{seat}': ${bet_type_amount[seat]}", end='')
                            else:
                                print(f"\n    '{seat}': {bet_type_amount[seat]}", end='')
                        elif ((key == 'main_bet_amounts') and (self.player_has_no_main_bets_in_play())):
                            print(" None", end='')
                            break
                        elif ((key == 'side_bet_amounts') and (self.player_has_no_side_bets_in_play())):
                            print(" None", end='')
                            break
                        else:
                            if ((seat_number != None) and (bet_type_amount[seat] != None) and (bet_type_amount[seat] != 0)):
                                print(f"\n    '{seat}': ${bet_type_amount[seat]}", end='')
                    print("")
                case 'hands' | 'hand_scores':
                    print(f"{key}:", end='')
                    key_type = getattr(self, key) # player.hands or player.hand_scores
                    for seat, seat_number in self.occupied_seats.items():
                        if (flag == 'v'):
                            print(f"\n    '{seat}': {key_type[seat]}", end='')
                        elif self.player_has_no_cards_in_play():
                            print(" None", end='')
                            break
                        else:
                            if ((seat_number != None) and (key_type[seat] != None)):
                                if ((key != 'hands') and (key_type[seat] != [])):
                                    print(f"\n    '{seat}': {key_type[seat]}", end='')
                    print("")
                case other:
                    print(f"{key}: {value}")
        print("*  *  *  *  *")

    def print_player_chip_pool(self):
        displayed_bet = {}
        for chip_color, chip_count in self.chips.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(f"{self.name}'s ${self.chip_pool_balance} chip pool - {displayed_bet}")

    def print_current_bet(self, seat_name, side_bet_index):
        if side_bet_index == None:
            player_bet = self.main_bets[seat_name]
            player_bet_amount = self.main_bet_amounts[seat_name]
        else:
            player_bet = self.side_bets[seat_name][side_bet_index]
            player_bet_amount = self.side_bet_amounts[seat_name][side_bet_index]
        displayed_bet = {}
        for chip_color, chip_count in player_bet.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(f"{self.name}'s ${player_bet_amount} bet - {displayed_bet}")


    """
    def print_current_main_bet(self, seat):
        player_bet = self.main_bets[seat]
        displayed_bet = {}
        for chip_color, chip_count in player_bet.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(f"{self.name}'s ${self.main_bet_amounts[seat]} bet - {displayed_bet}")

    def print_current_side_bet(self, seat, side_bet_index):
        player_bet = self.side_bets[seat][side_bet_index]
        displayed_bet = {}
        for chip_color, chip_count in player_bet.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(f"{self.name}'s ${self.side_bet_amounts[seat][side_bet_index]} bet - {displayed_bet}")
    """

    # Whole number float cleanup helper functions
    def cast_whole_number_chip_pool_balance_to_int(self):
        chip_pool_balance_fraction = self.chip_pool_balance % 1
        if (chip_pool_balance_fraction == 0):
            self.chip_pool_balance = int(self.chip_pool_balance)

    def clean_up_fractions(self, seat_name, player_side_bet_index):
        # Clean up bet amounts /w trailing 0s for display --> 10.0 to 10, 3.0 to 3, etc.
        if player_side_bet_index == None:
            if self.main_bet_amounts[seat_name] != None:
                bet_amount_fraction = self.main_bet_amounts[seat_name] % 1
                if (bet_amount_fraction == 0):
                    self.main_bet_amounts[seat_name] = int(self.main_bet_amounts[seat_name])
        else:
            if self.side_bet_amounts[seat_name][player_side_bet_index] != None:
                bet_amount_fraction = self.side_bet_amounts[seat_name][player_side_bet_index] % 1
                if (bet_amount_fraction == 0):
                    self.side_bet_amounts[seat_name][player_side_bet_index] = (
                        int(self.side_bet_amounts[seat_name][player_side_bet_index]))
        # Clean up chip balance /w trailing 0s for display --> 98.0 to 98, etc.
        chip_pool_balance_fraction = self.chip_pool_balance % 1
        if (chip_pool_balance_fraction == 0):
            self.chip_pool_balance = int(self.chip_pool_balance)

    # Bet initialization helper functions
    def init_main_bet_fields(self, seat_name):
        empty_bet = dict.fromkeys(bjo.chip_names, 0)
        self.main_bets[seat_name] = empty_bet
        self.main_bet_amounts[seat_name] = 0
        self.main_bet_winnings[seat_name] = empty_bet
        self.main_bet_winnings_amounts[seat_name] = 0

    def init_side_bet_fields(self, seat_name, side_bet_name):
        self.placed_side_bet_names[seat_name].append(side_bet_name)
        empty_bet = dict.fromkeys(bjo.chip_names, 0)
        self.side_bets[seat_name].append(empty_bet)
        self.side_bet_amounts[seat_name].append(0)
        self.side_bet_winnings[seat_name].append(empty_bet)
        self.side_bet_winnings_amounts[seat_name].append(0)

    # Bet clear isn't needed unless Player moves seats or leaves the game

    # Bet manipulation helper functions
    def increase_current_bet(self, seat_name, player_side_bet_index, key):
        # Adapt this function to work for side bets
        chip_color = prutils.key_to_chip_default_bindings[key]
        if player_side_bet_index == None:
            player_bet = self.main_bets[seat_name]
        else:
            player_bet = self.side_bets[seat_name][player_side_bet_index]
        if (self.chips[chip_color] == 0):
            sys.stderr.write(f"Cannot add {chip_color} (${bjo.chips[chip_color]}) chip - not enough chips of this type in {self.name}'s chip pool!\n")
            self.print_player_chip_pool()
            print(f"Press 'g' to change cash to chips, 'c' to convert smaller chips into bigger ones, or 'b' to convert bigger chips into smaller ones")
        else:
            self.chips[chip_color] -= 1
            player_bet[chip_color] += 1
            chip_worth = bjo.chips[chip_color]
            self.chip_pool_balance -= chip_worth
            if player_side_bet_index == None:
                self.main_bet_amounts[seat_name] += chip_worth
            else:
                self.side_bet_amounts[seat_name][player_side_bet_index] += chip_worth
            self.clean_up_fractions(seat_name, player_side_bet_index)
            self.print_current_bet(seat_name, player_side_bet_index)
            #self.print_current_main_bet(seat_name)

    def decrease_current_bet(self, seat_name, player_side_bet_index, key):
        # Adapt this function to work for side bets
        chip_color = prutils.key_to_chip_decrement_bindings[key]
        if player_side_bet_index == None:
            player_bet = self.main_bets[seat_name]
        else:
            player_bet = self.side_bets[seat_name][player_side_bet_index]
        if player_bet[chip_color] > 0:
            player_bet[chip_color] -= 1
            self.chips[chip_color] += 1
            chip_worth = bjo.chips[chip_color]
            if player_side_bet_index == None:
                self.main_bet_amounts[seat_name] -= chip_worth
            else:
                self.side_bet_amounts[seat_name][player_side_bet_index] -= chip_worth
            self.chip_pool_balance += chip_worth
            self.clean_up_fractions(seat_name, player_side_bet_index)
            self.print_current_bet(seat_name, player_side_bet_index)
            #self.print_current_main_bet(seat_name)
    
    def reset_current_bet(self, seat_name, player_side_bet_index):
        # Adapt this function to work for side bets
        if player_side_bet_index == None:
            player_bet = self.main_bets[seat_name]
            player_bet_values = self.main_bet_amounts
        else:
            player_bet = self.side_bets[seat_name][player_side_bet_index]
            player_bet_values = self.side_bet_amounts
        #print(player_bet)
        for chip_color, chip_count in player_bet.items():
            chip_worth = bjo.chips[chip_color]
            self.chips[chip_color] += chip_count
            self.chip_pool_balance += chip_worth*chip_count
            """
            for chip in range(0, chip_count):
                self.chips[chip_color] += 1
                self.chip_pool_balance += chip_worth
            """
            player_bet[chip_color] = 0
        if player_side_bet_index == None:
            player_bet_values[seat_name] = 0
            self.clean_up_fractions(seat_name, player_side_bet_index)
            print(f"Reset {self.name}'s main bet to ${self.main_bet_amounts[seat_name]}!")
        else:
            player_bet_values[seat_name][player_side_bet_index] = 0
            self.clean_up_fractions(seat_name, player_side_bet_index)
            print(f"Reset {self.name}'s side bet of '{self.placed_side_bet_names[seat_name][player_side_bet_index]}'", end='')
            print(f" to ${self.side_bet_amounts[seat_name][player_side_bet_index]}!")
            

    def get_chips(self):
        pass

    def color_up(self):
        pass

    def break_down(self):
        pass

    def skip_bet(self):
        # Todo AB: Write out skip_bet()

        pass

    def add_seat(self): # Todo AB: How to propagate seat adding/moving/leaving to blackjack_fsm.py
        pass

    def move_seat(self):
        pass

    def leave_seat(self):
        pass

    """
    def leave_table(self):
        pass
    """

    """
    def get_single_character(self):
        char = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        #char = input("")
        print(char)
    """


    def get_bet_input_character(self, min_bet, max_bet, seat_name, player_side_bet_index):
        # Todo AB: Make sure the above code scales with player making multiple hand bets
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                prutils.view_chip_betting_interface()
            case 'd':
                self.print_player_chip_pool()
            case 'p':
                self.print_current_bet(seat_name, player_side_bet_index)
            case 'r':
                self.reset_current_bet(seat_name, player_side_bet_index)
            case 'f':
                if player_side_bet_index == None:
                    player_bet_value = self.main_bet_amounts[seat_name]
                else:
                    player_bet_value = self.side_bet_amounts[seat_name][player_side_bet_index]
                fraction = player_bet_value % 1
                if (fraction != 0):
                    sys.stderr.write(f"Invalid (fractional) bet amount of ${player_bet_value} - please resubmit a bet /w an even number of Pink chips!\n")
                elif (player_bet_value < min_bet):
                    sys.stderr.write(f"{self.name}'s ${player_bet_value} bet is below allowed minimum, please submit a bet between inclusive bounds of ${min_bet} and ${max_bet}\n")
                elif (player_bet_value > max_bet):
                    sys.stderr.write(f"{self.name}'s ${player_bet_value} bet is above allowed maximum, please submit a bet between inclusive bounds of ${min_bet} and ${max_bet}\n")
                else:
                    return True # finalize bet for current seat
            case 's':
                self.skip_bet(seat_name, player_side_bet_index)
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.increase_current_bet(seat_name, player_side_bet_index, key)
                #prutils.print_player_chip_pool()
                #self.print_current_main_bet()
            case '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(':
                self.decrease_current_bet(seat_name, player_side_bet_index, key)
                #prutils.print_player_chip_pool()
                #self.print_current_main_bet()
            case 'g' | 'c' | 'b' | 'm' | 'a' | 'l':
                match key:
                    case 'g':
                        self.get_chips() # Todo AB: implement get_chips()
                    case 'c':
                        self.color_up() # Todo AB: implement color_up()
                    case 'b':
                        self.break_down() # Todo AB: implement break_down()
                    case 'm':
                        self.skip_bet() # Todo AB: implement skip_bet()
                    case 'a':
                        self.add_seat() # Todo AB: implement add_seat()
                    case 'l':
                        self.leave_seat() # Todo AB: implement leave_table()
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide a valid key or press 'v' to see valid key input options")

    """
    def get_main_bet_input_character(self, min_table_bet, max_table_bet, seat_name):
        # Todo AB: Make sure the above code scales with player making multiple hand bets
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                prutils.view_chip_betting_interface()
            case 'd':
                self.print_player_chip_pool()
            case 'p':
                self.print_current_main_bet(seat_name)
            case 'r':
                self.reset_current_bet(seat_name)
            case 'f':
                player_bet_value = self.main_bet_amounts[seat_name]
                fraction = player_bet_value % 1
                if (fraction != 0):
                    sys.stderr.write(f"Invalid (fractional) bet amount of ${player_bet_value} - please resubmit a bet /w an even number of Pink chips!\n")
                elif (player_bet_value < min_table_bet):
                    sys.stderr.write(f"{self.name}'s ${player_bet_value} bet is below allowed table minimum, please submit a bet between inclusive bounds of ${min_table_bet} and ${max_table_bet}\n")
                elif (player_bet_value > max_table_bet):
                    sys.stderr.write(f"{self.name}'s ${player_bet_value} bet is above allowed table maximum, please submit a bet between inclusive bounds of ${min_table_bet} and ${max_table_bet}\n")
                else:
                    return True # finalize bet for current seat
            case 's':
                self.skip_bet(seat_name)
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.increase_current_bet(seat_name, key)
                #prutils.print_player_chip_pool()
                #self.print_current_main_bet()
            case '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(':
                self.decrease_current_bet(seat_name, key)
                #prutils.print_player_chip_pool()
                #self.print_current_main_bet()
            case 'g' | 'c' | 'b' | 'm' | 'a' | 'l':
                match key:
                    case 'g':
                        self.get_chips() # Todo AB: implement get_chips()
                    case 'c':
                        self.color_up() # Todo AB: implement color_up()
                    case 'b':
                        self.break_down() # Todo AB: implement break_down()
                    case 'm':
                        self.skip_bet() # Todo AB: implement skip_bet()
                    case 'a':
                        self.add_seat() # Todo AB: implement add_seat()
                    case 'l':
                        self.leave_seat() # Todo AB: implement leave_table()
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide a valid key or press 'v' to see valid key input options")


    def get_side_bet_input_character(self, min_side_bet, max_side_bet, seat_name, side_bet_index):
        # Todo AB: Make sure the above code scales with player making multiple hand bets
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                prutils.view_chip_betting_interface()
            case 'd':
                self.print_player_chip_pool()
            case 'p':
                self.print_current_side_bet(seat_name, side_bet_index)
            case 'r':
                self.reset_current_bet(seat_name)
            case 'f':
                player_bet_value = self.main_bet_amounts[seat_name]
                fraction = player_bet_value % 1
                if (fraction != 0):
                    sys.stderr.write(f"Invalid (fractional) bet amount of ${player_bet_value} - please resubmit a bet /w an even number of Pink chips!\n")
                elif (player_bet_value < min_side_bet):
                    sys.stderr.write(f"{self.name}'s ${player_bet_value} bet is below allowed side bet minimum, please submit a bet between inclusive bounds of ${min_side_bet} and ${max_side_bet}\n")
                elif (player_bet_value > max_side_bet):
                    sys.stderr.write(f"{self.name}'s ${player_bet_value} bet is above allowed side bet maximum, please submit a bet between inclusive bounds of ${min_side_bet} and ${max_side_bet}\n")
                else:
                    return True # finalize bet for current seat
            case 's':
                self.skip_bet(seat_name)
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.increase_current_bet(seat_name, key)
                #prutils.print_player_chip_pool()
                #self.print_current_main_bet()
            case '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(':
                self.decrease_current_bet(seat_name, key)
                #prutils.print_player_chip_pool()
                #self.print_current_main_bet()
            case 'g' | 'c' | 'b' | 'm' | 'a' | 'l':
                match key:
                    case 'g':
                        self.get_chips() # Todo AB: implement get_chips()
                    case 'c':
                        self.color_up() # Todo AB: implement color_up()
                    case 'b':
                        self.break_down() # Todo AB: implement break_down()
                    case 'm':
                        self.skip_bet() # Todo AB: implement skip_bet()
                    case 'a':
                        self.add_seat() # Todo AB: implement add_seat()
                    case 'l':
                        self.leave_seat() # Todo AB: implement leave_table()
            case other:
                sys.stderr.write(f"Invalid input '{key}'\n")
                print("Provide a valid key or press 'v' to see valid key input options")
    """