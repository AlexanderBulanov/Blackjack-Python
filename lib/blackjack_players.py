""" 
File: blackjack_players.py
Author: Alexander Bulanov
"""

# Global Imports


# Local Imports #


### Defining Players for Tracking ###
class Player:
    def __init__(self):
        self.name = None # assign when new player is created
        self.has_priority = False # update to True/False as priority passes
        self.is_dealer = False
        self.current_balance = None
        self.White = 0
        self.Pink = 0
        self.Red = 0
        self.Blue = 0
        self.Green = 0
        self.Black = 0
        self.Purple = 0
        self.Yellow = 0
        self.Brown = 0
        self.current_hands = []
        self.current_hand_scores = [0]
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
        Dealer.has_priority = False
        Dealer.is_dealer = True
        Dealer.current_balance = 10000
        Dealer.White = 1000
        Dealer.Pink = 1000
        Dealer.Red = 1000
        Dealer.Blue = 1000
        Dealer.Green = 1000
        Dealer.Black = 1000
        Dealer.Purple = 1000
        Dealer.Yellow = 1000
        Dealer.Brown = 1000
        Dealer.current_hands = []
        Dealer.current_hand_scores = [0]
        Dealer.action = None
        return Dealer
    
    def create_new_player_from_template(player_name):
        NewPlayer = Player()
        NewPlayer.name = player_name
        NewPlayer.has_priority = False
        NewPlayer.is_dealer = False
        NewPlayer.current_balance = 100
        NewPlayer.White = 50
        NewPlayer.Pink = 0
        NewPlayer.Red = 30
        NewPlayer.Blue = 20
        NewPlayer.Green = 4
        NewPlayer.Black = 0
        NewPlayer.Purple = 0
        NewPlayer.Yellow = 0
        NewPlayer.Brown = 0
        NewPlayer.current_hands = []
        NewPlayer.current_hand_scores = [0]
        NewPlayer.action = None
        return NewPlayer
    
    def print_player_stats(self):
        print("*  *  *")
        if self.name == 'Dealer':
            print("Printing Dealer Statistics")
        else:
            print("Printing Statistics for Player '"+self.name+"'")
        for key, value in self.__dict__.items():
            if key == 'current_balance':
                print(str(key)+": $"+str(value))
            else:
                print(str(key)+": "+str(value))
        print("*  *  *")