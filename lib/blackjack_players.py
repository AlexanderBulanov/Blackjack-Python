""" 
File: blackjack_players.py
Author: Alexander Bulanov
"""

# Global Imports #
from msvcrt import getch

# Local Imports #
from . import blackjack_game_objects as bjo

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

# Custom Exceptions #
class ExitBettingInterface(Exception):
    pass

### Defining Players for Tracking ###
class Player:
    def __init__(self):
        self.name = None
        self.is_dealer = False
        self.current_cash_balance = None
        self.chips = dict.fromkeys(bjo.chip_names, 0)
        self.chip_pool_balance = 0
        self.hole_card_face_down = False
        self.current_main_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
        }
        self.current_main_bet_amounts = {
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
        }
        self.current_side_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
        }
        self.current_side_bet_amounts = {
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
        }
        self.current_hands = { # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
        }
        self.current_hand_scores = {
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
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
        Dealer.current_cash_balance = 10000
        Dealer.chips = dict.fromkeys(bjo.chip_names, 1000)
        Dealer.chip_pool_balance = 1000*(1+2.5+5+10+25+100+500+1000+5000)
        Dealer.hole_card_face_down = True
        Dealer.current_main_bets = { # each bet is stored as a dictionary in format of chip_color: chip_count
            'left_seat': None,
            'current_seat': 0,
            'right_seat': None
        }
        Dealer.current_main_bet_amounts = {
            'left_seat': None,
            'current_seat': None,
            'right_seat': None
        }
        Dealer.current_side_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        Dealer.current_side_bet_amounts = []
        Dealer.current_hands = [] # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
        Dealer.current_hand_scores = []
        Dealer.action = None
        return Dealer
    
    def create_new_player_from_template(player_name):
        NewPlayer = Player()
        NewPlayer.name = player_name
        NewPlayer.is_dealer = False
        NewPlayer.current_cash_balance = 100
        NewPlayer.chips = dict.fromkeys(bjo.chip_names, 0)
        NewPlayer.chips['White'] = 50
        NewPlayer.chips['Pink'] = 30
        NewPlayer.chips['Red'] = 20
        NewPlayer.chips['Blue'] = 15
        NewPlayer.chips['Green'] = 5
        NewPlayer.chip_pool_balance = int(50*1 + 30*2.5 + 20*5 + 15*10 + 5*25)
        NewPlayer.hole_card_face_down = False
        NewPlayer.current_main_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        NewPlayer.current_main_bet_amounts = []
        NewPlayer.current_side_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        NewPlayer.current_side_bet_amounts = []
        NewPlayer.current_hands = [] # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
        NewPlayer.current_hand_scores = []
        NewPlayer.action = None
        return NewPlayer
    
    def print_player_stats(self):
        print("*  *  *  *  *")
        if self.name == 'Dealer':
            print("Printing Dealer Statistics")
        else:
            print("Printing Statistics for Player '"+self.name+"'")
        for key, value in self.__dict__.items():
            if (key == 'current_cash_balance') or (key == 'chip_pool_balance'):
                print(str(key)+": $"+str(value))
            elif (key == 'current_hands') and (self.hole_card_face_down == True):
                hands = "["
                if (len(self.current_hands) == 0):
                    hands = hands+"]"
                else:
                    for hand in self.current_hands:
                        face_up_card = hand[0]
                        if (self.current_hands.index(hand) == (len(self.current_hands) - 1)):
                            hands = hands+"["+str(face_up_card)+", '**']]"
                        else:
                            hands = hands+"["+str(face_up_card)+", '**'], "
                # Print hole card as '**'
                print(str(key)+": "+hands)
            else:
                print(str(key)+": "+str(value))
        print("*  *  *  *  *")

    def display_player_chip_pool(self):
        print(f"{self.name}'s ${self.chip_pool_balance} chip pool - ", end='')
        displayed_bet = {}
        for chip_color, chip_count in self.chips.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(displayed_bet)

    # Helper methods
    def clean_up_fractions(self):
        bet_amount_fraction = self.current_main_bet_amounts[-1] % 1
        chip_pool_balance_fraction = self.chip_pool_balance % 1
        if (bet_amount_fraction == 0):
            self.current_main_bet_amounts[-1] = int(self.current_main_bet_amounts[-1])
        if (chip_pool_balance_fraction == 0):
            self.chip_pool_balance = int(self.chip_pool_balance)

    def print_current_bet(self):
        print(f"{self.name}'s ${self.current_main_bet_amounts[-1]} bet - ", end='')
        player_bet = self.current_main_bets[0]
        displayed_bet = {}
        for chip_color, chip_count in player_bet.items():
            if (chip_count > 0):
                displayed_bet[chip_color] = chip_count
        print(displayed_bet)

    def increase_current_bet(self, key):
        chip_color = key_to_chip_default_bindings[key]
        player_bet = self.current_main_bets[0]
        if (self.chips[chip_color] == 0):
            print(f"Cannot add {chip_color} (${bjo.chips[chip_color]}) chip - not enough chips of this type in {self.name}'s chip pool!")
            self.display_player_chip_pool()
            print(f"Enter 'g' to exchange cash to chips, 'c' to convert smaller chips into bigger ones, or 'b' to convert bigger chips into smaller ones")
        else:
            self.chips[chip_color] -= 1
            player_bet[chip_color] += 1
            chip_worth = bjo.chips[chip_color]
            self.current_main_bet_amounts[-1] += chip_worth
            self.chip_pool_balance -= chip_worth
            self.clean_up_fractions()
            self.print_current_bet()

    def decrease_current_bet(self, key):
        chip_color = key_to_chip_decrement_bindings[key]
        player_bet = self.current_main_bets[0]
        if player_bet[chip_color] > 0:
            player_bet[chip_color] -= 1
            self.chips[chip_color] += 1
            chip_worth = bjo.chips[chip_color]
            self.current_main_bet_amounts[-1] -= chip_worth
            self.chip_pool_balance += chip_worth
            self.clean_up_fractions()
            self.print_current_bet()
    
    def reset_current_bet(self):
        player_bet = self.current_main_bets[0]
        player_bet_values = self.current_main_bet_amounts
        #print(player_bet)
        for chip_color, chip_count in player_bet.items():
            chip_worth = bjo.chips[chip_color]
            for chip in range(0, chip_count):
                self.chips[chip_color] += 1
                self.chip_pool_balance += chip_worth
            player_bet[chip_color] = 0
            player_bet_values[0] = 0
        self.clean_up_fractions()
        print(f"Reset {self.name}'s bet to ${self.current_main_bet_amounts[-1]}!")

    def get_chips(self):
        pass

    def color_up(self):
        pass

    def break_down(self):
        pass

    def skip_bet(self):
        pass

    def add_seat(self):
        pass

    def move_seat(self):
        pass

    def leave_seat(self):
        pass

    """
    def leave_table(self):
        pass
    """


    def get_bet_input_character(self, min_bet, max_bet):
        # Todo AB: Make sure the above code scales with player making multiple hand bets

        key = getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'v':
                self.view_betting_interface()
            case 'd':
                self.display_player_chip_pool()
            case 'p':
                self.print_current_bet()
            case 'r':
                self.reset_current_bet()
            case 'f':
                player_bet_value = self.current_main_bet_amounts[-1]
                fraction = player_bet_value % 1
                if (fraction != 0):
                    print(f"Invalid (fractional) bet amount of ${player_bet_value} - please resubmit a bet /w an even number of Pink chips!")
                elif (player_bet_value < min_bet):
                    print(f"{self.name}'s ${player_bet_value} bet is below table minimum, please submit a bet between inclusive bounds of ${min_bet} and ${max_bet}")
                elif (player_bet_value > max_bet):
                    print(f"{self.name}'s ${player_bet_value} bet is above table maximum, please submit a bet between inclusive bounds of ${min_bet} and ${max_bet}")
                else:
                    raise ExitBettingInterface
            case 's':
                self.skip_bet()
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                self.increase_current_bet(key)
                #self.display_player_chip_pool()
                #self.print_current_bet()
            case '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(':
                self.decrease_current_bet(key)
                #self.display_player_chip_pool()
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


        """
        if (int(chip_keybind)-1) < len(other_keybindings_list):
            self.print_betting_interface_padding(chip_color)
            other_keybind = other_keybindings_list[int(chip_keybind)-1]
            print(f"{other_keybind}: {special_key_bindings[other_keybind]}")
        else:
            print("")
        """


    def view_betting_interface(self):
        print("Press the following number keys to add chips, symbol keys to remove chips, and letter keys to execute special actions:")
        for chip_keybind, chip_color in key_to_chip_default_bindings.items():
            print(f"{chip_keybind}: +${bjo.chips[chip_color]} ({chip_color})", end='')
            self.print_betting_interface_padding(chip_color)
            chip_decrement_keybind = list(key_to_chip_decrement_bindings.keys())[int(chip_keybind)-1]
            print(f"{chip_decrement_keybind}: -${bjo.chips[chip_color]} ({chip_color})", end='')
            self.print_letter_keybinding(chip_keybind, chip_color)


    def get_player_bet(self, table_seat, min_bet, max_bet): # Todo AB: Incorporate table_seat

        empty_bet = dict.fromkeys(bjo.chip_names, 0)
        self.current_main_bets.append(empty_bet) # Add a new empty chip dictionary to track a new bet
        self.current_main_bet_amounts.append(0) # Initialize value of a new bet to 0
        self.view_betting_interface()
        self.display_player_chip_pool()
        try:
            while True:
                self.get_bet_input_character(min_bet, max_bet)
        except ExitBettingInterface:
            print("Exiting betting interface...\n")