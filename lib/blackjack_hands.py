""" 
File: blackjack_hands.py
Author: Alexander Bulanov
"""

# Global Imports #


# Local Imports #


### Defining Hands for Tracking Primary and Side Bets ###
class Hand:
    def __init__(self):
        self.cards = []
        self.score = 0
        self.bet_total = None
        self.insurance = False # May need to handle these separately
        self.even_money = False # May need to handle these separately
        self.White = 0
        self.Pink = 0
        self.Red = 0
        self.Blue = 0
        self.Green = 0
        self.Black = 0
        self.Purple = 0
        self.Yellow = 0
        self.Brown = 0