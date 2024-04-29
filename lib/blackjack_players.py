""" 
File: blackjack_players.py
Author: Alexander Bulanov
"""

# Global Imports #


# Local Imports #
from msvcrt import getch

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
        self.current_primary_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        self.current_primary_bet_values = []
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
        Dealer.current_primary_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        Dealer.current_primary_bet_values = []
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
        NewPlayer.current_primary_bets = [] # each bet is stored as a dictionary in format of chip_color: chip_count
        NewPlayer.current_primary_bet_values = []
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


    def add_primary_bet(self, hand, bet_string): # Example of bet_string --> '2 White, 1 Blue'
        hand_index = self.current_hands.index(hand)
        if (hand_index == 0):
            self.current_primary_bets.append({})
            for chip_phrase in bet_string.split(", "):
                chip_color, chip_count = chip_phrase.split()
                self.current_primary_bets[0][chip_color] = chip_count
        else:
            for index in range(0, self.current_hands.index(hand)-1):
                self.current_primary_bets.append({})
            self.current_primary_bets.append({})
            for chip_phrase in bet_string.split(", "):
                chip_color, chip_count = chip_phrase.split()
                self.current_primary_bets[hand_index][chip_color] = chip_count



    def get_player_bet(self):
        key_to_chip_mappings = {
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

        print("Press keys 1-9 to add the following chips or 0 for separate menu")
        key = getch()

        match key:
            case '0':
                # Reset to enter a diffent bet
                pass
            case '1':
                pass
            case '2':
                pass
            case '3':
                pass
            case '4':
                pass
            case '5':
                pass
            case '6':
                pass
            case '7':
                pass
            case '8':
                pass
            case '9':
                pass
            case other:
                print("Invalid input. Press the following numbers to add chips:")
                print("1 - White ($1)")
                print("2 - Pink ($2.5)")
                print("3 - Red ($5)")
                print("4 - Blue ($10)")
                print("5 - Green ($25)")
                print("6 - Black ($100)")
                print("7 - Purple ($500)")
                print("8 - Yellow ($1000)")
                print("9 - Brown ($5000)")