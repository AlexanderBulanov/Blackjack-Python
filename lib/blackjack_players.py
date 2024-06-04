""" 
File: blackjack_players.py
Author: Alexander Bulanov
"""

# Global Imports #
import msvcrt
import logging

# Local Imports #
from . import blackjack_game_objects as bjo

# Configuration for Logging #
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Global-scope reference objects #
key_to_chip_default_bindings = {
    '1': 'White',
    '2': 'Pink',
    '3': 'Red',
    '4': 'Blue',
    '5': 'Green',
    '6': 'Black',
    '7': 'Purple',
    '8': 'Yellow',
    '9': 'Brown',
}

key_to_chip_decrement_bindings = {
    '!': 'White',
    '@': 'Pink',
    '#': 'Red',
    '$': 'Blue',
    '%': 'Green',
    '^': 'Black',
    '&': 'Purple',
    '*': 'Yellow',
    '(': 'Brown',
}

special_key_bindings = {
    'v': 'view betting interface',
    'd': 'display player chip pool',
    'p': 'print current bet',
    'r': 'reset current bet',
    'f': 'finish current bet',
    's': 'skip betting',
    'g': 'get chips',
    'c': 'color up',
    'b': 'break down',
    'm': 'move seat',
    'a': 'add seat',
    'l': 'leave seat',
}

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
        self.side_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        self.side_bet_amounts = { # each bet amount is stored as an integer (betting of $2.5 chips is restricted to pairs only)
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
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
        Dealer.chip_pool_balance = 1000*(1+2.5+5+10+25+100+500+1000+5000)
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
        Dealer.side_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        Dealer.side_bet_amounts = { # each bet amount is stored as an integer (betting of $2.5 chips is restricted to pairs only)
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
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
        NewPlayer.side_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
        }
        NewPlayer.side_bet_amounts = { # each bet amount is stored as an integer (betting of $2.5 chips is restricted to pairs only)
            'right_seat': None,
            'center_seat': None,
            'left_seat': None,
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
                    bet_type = getattr(self, key) # self.main_bets or self.side_bets
                    for seat, seat_number in self.occupied_seats.items():
                        if (flag == 'v'):
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
                                for chip_color, chip_count in bet_type[seat].items():
                                    if (chip_count != 0):
                                        non_zero_bet_chips[chip_color] = chip_count
                                print(f"\n    '{seat}': {non_zero_bet_chips}", end='')
                    print("")
                case 'main_bet_amounts' | 'side_bet_amounts':
                    print(f"{key}:", end='')
                    bet_type_amount = getattr(self, key) # self.main_bet_amounts or self.side_bet_amounts
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
                    key_type = getattr(self, key) # self.hands or self.hand_scores
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

    def get_player_chip_pool_message(self):
        displayed_bet = {}
        for chip_color, chip_count in self.chips.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        return f"{self.name}'s ${self.chip_pool_balance} chip pool - {displayed_bet}"

    # Helper methods
    def clean_up_fractions(self, seat):
        bet_amount_fraction = self.main_bet_amounts[seat] % 1
        chip_pool_balance_fraction = self.chip_pool_balance % 1
        if (bet_amount_fraction == 0):
            self.main_bet_amounts[seat] = int(self.main_bet_amounts[seat])
        if (chip_pool_balance_fraction == 0):
            self.chip_pool_balance = int(self.chip_pool_balance)

    def print_current_bet(self, seat):
        print(f"{self.name}'s ${self.main_bet_amounts[seat]} bet - ", end='')
        player_bet = self.main_bets[seat]
        displayed_bet = {}
        for chip_color, chip_count in player_bet.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(displayed_bet)

    def increase_current_bet(self, seat, key):
        chip_color = key_to_chip_default_bindings[key]
        player_bet = self.main_bets[seat]
        if (self.chips[chip_color] == 0):
            logger.error(f"Cannot add {chip_color} (${bjo.chips[chip_color]}) chip - not enough chips of this type in {self.name}'s chip pool!")
            logger.info(self.get_player_chip_pool_message())
            logger.info(f"Press 'g' to change cash to chips, 'c' to convert smaller chips into bigger ones, or 'b' to convert bigger chips into smaller ones")
        else:
            self.chips[chip_color] -= 1
            player_bet[chip_color] += 1
            chip_worth = bjo.chips[chip_color]
            self.main_bet_amounts[seat] += chip_worth
            self.chip_pool_balance -= chip_worth
            self.clean_up_fractions(seat)
            self.print_current_bet(seat)

    def decrease_current_bet(self, seat, key):
        chip_color = key_to_chip_decrement_bindings[key]
        player_bet = self.main_bets[seat]
        if player_bet[chip_color] > 0:
            player_bet[chip_color] -= 1
            self.chips[chip_color] += 1
            chip_worth = bjo.chips[chip_color]
            self.main_bet_amounts[seat] -= chip_worth
            self.chip_pool_balance += chip_worth
            self.clean_up_fractions(seat)
            self.print_current_bet(seat)
    
    def reset_current_bet(self, seat):
        player_bet = self.main_bets[seat]
        player_bet_values = self.main_bet_amounts
        #print(player_bet)
        for chip_color, chip_count in player_bet.items():
            chip_worth = bjo.chips[chip_color]
            for chip in range(0, chip_count):
                self.chips[chip_color] += 1
                self.chip_pool_balance += chip_worth
            player_bet[chip_color] = 0
            player_bet_values[seat] = 0
        self.clean_up_fractions(seat)
        print(f"Reset {self.name}'s bet to ${self.main_bet_amounts[seat]}!")

    def get_chips(self):
        pass

    def color_up(self):
        pass

    def break_down(self):
        pass

    def skip_bet(self):
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


    def get_bet_input_character(self, min_bet, max_bet, seat):
        # Todo AB: Make sure the above code scales with player making multiple hand bets
        key = msvcrt.getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                self.view_betting_interface()
            case 'd':
                logger.info(self.get_player_chip_pool_message())
            case 'p':
                self.print_current_bet(seat)
            case 'r':
                self.reset_current_bet(seat)
            case 'f':
                player_bet_value = self.main_bet_amounts[seat]
                fraction = player_bet_value % 1
                if (fraction != 0):
                    print(f"Invalid (fractional) bet amount of ${player_bet_value} - please resubmit a bet /w an even number of Pink chips!")
                elif (player_bet_value < min_bet):
                    print(f"{self.name}'s ${player_bet_value} bet is below table minimum, please submit a bet between inclusive bounds of ${min_bet} and ${max_bet}")
                elif (player_bet_value > max_bet):
                    print(f"{self.name}'s ${player_bet_value} bet is above table maximum, please submit a bet between inclusive bounds of ${min_bet} and ${max_bet}")
                else:
                    return True # finalize bet for current seat
            case 's':
                self.skip_bet(seat)
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.increase_current_bet(seat, key)
                #logger.info(self.get_player_chip_pool_message())
                #self.print_current_bet()
            case '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(':
                self.decrease_current_bet(seat, key)
                #logger.info(self.get_player_chip_pool_message())
                #self.print_current_bet()
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
                print(f"Invalid input '{key}'")
                print("Provide a valid key or press 'v' to see valid key input options")


    def print_betting_interface_padding(self, chip_color):
        padding_spaces = 14
        for char in str(bjo.chips[chip_color]):
            padding_spaces -= 1
        for char in chip_color:
            padding_spaces -= 1
        for num in range(0, padding_spaces):
            print(" ", end='')


    def print_letter_keybinding(self, chip_keybind, chip_color):
        if ((int(chip_keybind)-1) < 6):
            other_keybindings_list = list(special_key_bindings.keys())
            # Print 6 keybindings in one column, then 6 more in the padded one to the right
            self.print_betting_interface_padding(chip_color)
            other_keybind_col_one = other_keybindings_list[int(chip_keybind)-1]
            print(f"{other_keybind_col_one}: {special_key_bindings[other_keybind_col_one]}", end='')
            padding_spaces = 28
            other_keybinding_names = list(special_key_bindings.values())
            other_keybinding_name = other_keybinding_names[int(chip_keybind)-1]
            #print(repr(other_keybinding_name))
            for char in other_keybinding_name:
                padding_spaces -= 1
            #print(padding_spaces, end='')
            for num in range(0, padding_spaces):
                print(" ", end='')
            other_keybind_col_two = other_keybindings_list[int(chip_keybind)-1+6]
            print(f"{other_keybind_col_two}: {special_key_bindings[other_keybind_col_two]}")
        else:
            print("")


    def view_betting_interface(self):
        print("Press the following number keys to add chips, symbol keys to remove chips, and letter keys to execute special actions:")
        for chip_keybind, chip_color in key_to_chip_default_bindings.items():
            print(f"{chip_keybind}: +${bjo.chips[chip_color]} ({chip_color})", end='')
            self.print_betting_interface_padding(chip_color)
            chip_decrement_keybind = list(key_to_chip_decrement_bindings.keys())[int(chip_keybind)-1]
            print(f"{chip_decrement_keybind}: -${bjo.chips[chip_color]} ({chip_color})", end='')
            self.print_letter_keybinding(chip_keybind, chip_color)

    def init_main_seat_bet_fields(self, seat_name):
        empty_bet = dict.fromkeys(bjo.chip_names, 0)
        self.main_bets[seat_name] = empty_bet
        self.main_bet_amounts[seat_name] = 0

    def get_bets_from_all_one_player_occupied_seats(self, min_bet, max_bet):
        for seat_name, seat_pos in self.occupied_seats.items():
            if (seat_pos != None): # Get each player's bets from up to 3 seats they can occupy
                self.init_main_seat_bet_fields(seat_name)
                print(f"Player '{self.name}' betting at Seat #{seat_pos} (their '{seat_name}')")
                self.view_betting_interface()
                logger.info(self.get_player_chip_pool_message())
                while True: # Using this format instead of try-except and custom exception ExitBettingInterface, to pass tests
                    if self.get_bet_input_character(min_bet, max_bet, seat_name): 
                        print("Exiting betting interface...")
                        break