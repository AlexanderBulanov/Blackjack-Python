""" 
File: blackjack_game_objects.py
Author: Alexander Bulanov
"""

### Imports ###
import random


### Game Objects ###
# Chips and their values #
chip_names = ['White', 'Pink', 'Red', 'Blue', 'Green', 'Black', 'Purple', 'Yellow', 'Brown']
chip_values = [1, 2.5, 5, 10, 25, 100, 500, 1000, 5000]
chips = dict(zip(chip_names,chip_values))

# Cards and their values #
card_names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_values = [[2], [3], [4], [5], [6], [7], [8], [9], [10], [10], [10], [10], [1, 11]]
cards = dict(zip(card_names,card_values))

# Card Suits #
suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

# Base Deck (as reference) #
base_deck = []
for s in suit_names:
    for c in card_names:
        base_deck.extend([c+s[0]])
random.shuffle(base_deck)

### Game Object Constructors ###
def get_shoe_of_n_decks(n):
    shoe = []
    for s in suit_names:
        for c in card_names:
            for count in range(0, n):
                shoe.extend([c+s[0]])
    random.shuffle(shoe)
    return shoe