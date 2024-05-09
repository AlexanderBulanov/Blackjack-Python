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
    'r': 'reset bet',
    'f': 'finish bet',
    'p': 'print betting interface',
    'd': 'display current bet',
    'c': 'color up',
    'b': 'break down',
    's': 'skip bet', # Todo AB: switch seat?
    'l': 'leave table'
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
        self.White = 0
        self.Pink = 0
        self.Red = 0
        self.Blue = 0
        self.Green = 0
        self.Black = 0
        self.Purple = 0
        self.Yellow = 0
        self.Brown = 0
        self.hole_card_face_down = False
        self.current_main_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        self.current_main_bet_values = []
        self.current_side_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        self.current_side_bet_values = []
        self.current_hands = [] # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
        self.current_hand_scores = []
        self.action = None

    # Player actions are:
        # Out-of-Round:
            # Join
            # Leave
        # In-Round (Main Bets):
            # Place a Bet
            # Stand
            # Hit
            # Double-Down
            # Split
            # Surrender
        # In-Round (Side Bets):
            # Insurance
            # Even Money

    def create_casino_dealer():
        Dealer = Player()
        Dealer.name = 'Dealer'
        Dealer.is_dealer = True
        Dealer.current_cash_balance = 10000
        Dealer.White = 1000
        Dealer.Pink = 1000
        Dealer.Red = 1000
        Dealer.Blue = 1000
        Dealer.Green = 1000
        Dealer.Black = 1000
        Dealer.Purple = 1000
        Dealer.Yellow = 1000
        Dealer.Brown = 1000
        Dealer.hole_card_face_down = True
        Dealer.current_main_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        Dealer.current_main_bet_values = []
        Dealer.current_side_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        Dealer.current_side_bet_values = []
        Dealer.current_hands = [] # each hand is stored as a list of shorthand card names, such as ['8H', 'JC']
        Dealer.current_hand_scores = []
        Dealer.action = None
        return Dealer
    
    def create_new_player_from_template(player_name):
        NewPlayer = Player()
        NewPlayer.name = player_name
        NewPlayer.is_dealer = False
        NewPlayer.current_cash_balance = 100
        NewPlayer.White = 50
        NewPlayer.Pink = 0
        NewPlayer.Red = 30
        NewPlayer.Blue = 20
        NewPlayer.Green = 4
        NewPlayer.Black = 0
        NewPlayer.Purple = 0
        NewPlayer.Yellow = 0
        NewPlayer.Brown = 0
        NewPlayer.hole_card_face_down = False
        NewPlayer.current_main_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        NewPlayer.current_main_bet_values = []
        NewPlayer.current_side_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        NewPlayer.current_side_bet_values = []
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
            if (key == 'current_cash_balance'):
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


    # Helper methods
    def display_current_bet(self):
        print(f"{self.name}'s ${self.current_main_bet_values[-1]} bet - ", end='')
        print("{", end='')
        player_bet = self.current_main_bets[0]
        for chip_color, chip_count in player_bet.items():
            if (chip_count > 0):
                print(f"'{chip_color}': {chip_count}", end='')
                # Todo AB: if this is not the last key:value pair, print ", "
                
        print("}")

    def color_up(self):
        pass

    def break_down(self):
        pass

    def skip_bet(self):
        pass

    def leave_table(self):
        pass



    def get_bet_input_character(self):
        player_bet = self.current_main_bets[0]
        # Todo AB: Make sure the above code scales with player making multiple hand bets
        key = getch().decode('utf-8') # Get a key (as a byte string) and decode it
        match key:
            case 'r':
                for chip_color in player_bet.keys():
                    #print(f"Resetting chip color {chip_color} from {player_bet[chip_color]} chips to 0")
                    player_bet[chip_color] = 0
                print(f"Resetting {self.name}'s bet!")
                print(f"{self.name}'s bet - ", end='')
                print(player_bet)
            case 'f':
                #print("Special character 'f' entered!")
                raise ExitBettingInterface
            case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                chip_color = key_to_chip_default_bindings[key]
                player_bet[chip_color] += 1
                self.current_main_bet_values[-1] += bjo.chips[chip_color]
                # Todo AB: Provide a printing method to display only non-zero chip_color: chip_count key-value pairs


                print(f"{self.name}'s bet - ", end='')
                print(player_bet)
                print(f"Total bet value - {self.current_main_bet_values[-1]}")
            case '!' | '@' | '#' | '$' | '%' | '^' | '&' | '*' | '(':
                chip_color = key_to_chip_decrement_bindings[key]
                if player_bet[chip_color] > 0:
                    player_bet[chip_color] -= 1
                    self.current_main_bet_values[-1] -= bjo.chips[chip_color]
                    print(f"{self.name}'s bet - ", end='')
                    print(player_bet)
                    print(f"Total bet value - {self.current_main_bet_values[-1]}")
            case 'p' | 'd' | 'c' | 'b' | 's' | 'l':
                #print(f"Special character '{key}' entered!")
                match key:
                    case 'p':
                        self.print_betting_prompt()
                    case 'd':
                        self.display_current_bet()
                    case 'c':
                        self.color_up() # Todo AB: implement color_up()
                    case 'b':
                        self.break_down() # Todo AB: implement break_down()
                    case 's':
                        self.skip_bet() # Todo AB: implement skip_bet()
                    case 'l':
                        self.leave_table() # Todo AB: implement leave_table()
            case other:
                print(f"Invalid input '{key}'")
                self.print_betting_prompt()


    def print_betting_prompt_padding(self, chip_color):
        padding_spaces = 13
        for char in str(bjo.chips[chip_color]):
            padding_spaces -= 1
        for char in chip_color:
            padding_spaces -= 1
        for num in range(0, padding_spaces):
            print(" ", end='')


    def print_special_keybinding(self, chip_keybind, chip_color):
        other_keybindings_list = list(special_key_bindings.keys())
        if (int(chip_keybind)-1) < len(other_keybindings_list):
            self.print_betting_prompt_padding(chip_color)
            other_keybind = other_keybindings_list[int(chip_keybind)-1]
            print(f"{other_keybind}: {special_key_bindings[other_keybind]}")
        else:
            print("")


    def print_betting_prompt(self):
        print("Press the following number keys to add/remove chips or press letter keys for special actions:")
        for chip_keybind, chip_color in key_to_chip_default_bindings.items():
            print(f"{chip_keybind}: +${bjo.chips[chip_color]} ({chip_color})", end='')
            self.print_betting_prompt_padding(chip_color)
            chip_decrement_keybind = list(key_to_chip_decrement_bindings.keys())[int(chip_keybind)-1]
            print(f"{chip_decrement_keybind}: -${bjo.chips[chip_color]} ({chip_color})", end='')
            self.print_special_keybinding(chip_keybind, chip_color)
            # Todo AB: Possibly reimplement code below in print_special_keybindings(self, index) method above for visual clarity


    def get_player_bet(self):
        empty_bet = dict.fromkeys(bjo.chip_names, 0)
        self.current_main_bets.append(empty_bet) # Add a new empty chip dictionary to track a new bet
        self.current_main_bet_values.append(0) # Initialize value of a new bet to 0
        self.print_betting_prompt()
        try:
            while True:
                self.get_bet_input_character()
        except ExitBettingInterface:
            # Todo AB: Tally up how many
            print("Exiting betting interface...\n")