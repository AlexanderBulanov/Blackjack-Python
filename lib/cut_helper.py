""" 
File: cut_helper.py
Author: Alexander Bulanov
"""

# Global Imports #
import random
import math

# Local Imports #
from . import blackjack_game_settings as bjs

def first_cut(shoe):
    # Offer a player to insert 'back_cut_card' at least 15 cards deep from either edge
    
    # If no player chooses to make a cut, dealer announces they're making a cut and perform it as follows:

    # Placing the first cut card
    first_cut_card_index = random.randrange(15, len(shoe)-15, 1)
    #print("Placing 'back_cut_card' at index",first_cut_card_index)
    shoe.insert(first_cut_card_index,'back_cut_card')
    # Moving all cards starting with first cut card to the back of the card stack
    section = shoe[0:first_cut_card_index+1]
    del shoe[0:first_cut_card_index+1]
    shoe.extend(section)

def second_cut(shoe, manual_cut_percentage):
    # Identifying how much of a deck to cut off /w second cut card
    if (isinstance(manual_cut_percentage, int)):
        cut_percentage = manual_cut_percentage
        print("Manually setting cut percentage at "+str(manual_cut_percentage)+"%")
    else:
        #print("Shoe size is",len(shoe), "meaning it consists of",(len(shoe)-1)/52,"deck")
        lower_percent_bound = bjs.casino_deck_pen_percentage_bounds[(len(shoe)-1)/52][0]
        upper_percent_bound = bjs.casino_deck_pen_percentage_bounds[(len(shoe)-1)/52][1]
        cut_percentage = random.randrange(lower_percent_bound, upper_percent_bound, 1)
        print("Randomized cut percentage between bounds of "+
              str(lower_percent_bound)+"%"+" and "+str(upper_percent_bound)+"%"+" at "+str(cut_percentage)+"%")
    # Determining index to place the second cut card at
    unrounded_index = len(shoe)*(cut_percentage/100)
    rounded_index = math.floor(unrounded_index+0.5)
    second_cut_card_index = int(rounded_index)
    # Placing the second cut card
    #print("Placing 'front_cut_card' at index", second_cut_card_index)
    shoe.insert(second_cut_card_index,'front_cut_card')
    # Returning a value for State Machine to know what pen % is used for the game
    return cut_percentage