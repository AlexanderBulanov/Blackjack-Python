""" 
File: blackjack_game_logic.py
Author: Alexander Bulanov
"""

### Imports ###
import itertools
#import blackjack_game_objects as bjo
from . import blackjack_game_objects as bjo


### Functions ###
def highest_hand_score(player_hand):
    highest_hand_score = 0
    soft_hand = 0
    for card in player_hand:
        key = card[:-1] # key to access value of a card from bjo.cards dictionary
        low_value = bjo.cards[key][0] # 1-9 - 1-9, 10/J/Q/K - 10, A - 1
        high_value = bjo.cards[key][-1] # same as above, except A - 11
        # Case Group A - Hard Hands (w/o Aces at Value of 11)
        if (soft_hand == 0):
            # Case 1A - Hard hand, busts even on 1 from an Ace
            if (highest_hand_score+low_value > 21):
                return -1
            # Case 2A - Hard hand, adding a new Ace's low value makes Blackjack
            elif ((key == 'A') and (highest_hand_score+low_value == 21)):
                return 21
            # Case 3A - Hard hand, adding any non-Ace's high value makes Blackjack
            elif (highest_hand_score+high_value == 21):
                return 21
            # Case 4A - Hard hand, adding a new Ace's high value would bust
            elif ((key == 'A') and (highest_hand_score+high_value > 21)):
                highest_hand_score += low_value
            # Case 5A - Hard hand, adding any high card value doesn't bust or make Blackjack
            elif (highest_hand_score+high_value < 21):
                highest_hand_score += high_value
                # Update count of high-value aces in the hand as needed
                if (key == 'A'):
                    soft_hand += 1
        # Case Group B - Soft Hands (containing an Ace /w Value of 11)
        else:
            # Case 1B - Soft hand, adding a new Ace's low value makes Blackjack
            if ((key == 'A') and (highest_hand_score+low_value == 21)):
                return 21
            # Case 2B - Soft hand, adding any non-Ace's high value makes Blackjack
            elif ((key != 'A') and (highest_hand_score+high_value == 21)):
                return 21
            # Case 3B - Soft hand, adding a new Ace's high value would bust
            elif ((key == 'A') and (highest_hand_score+high_value > 21)):
                highest_hand_score += low_value
            # Case 4B - Soft hand, adding non-Ace's high value would bust
            elif ((key != 'A') and (highest_hand_score+high_value > 21)):
                highest_hand_score -= 10
                highest_hand_score += high_value
                soft_hand = 0
            # Case 5B - Soft hand, adding any non-Ace's high value doesn't bust or make Blackjack
            elif ((key != 'A') and (highest_hand_score+high_value < 21)):
                highest_hand_score += high_value
    return highest_hand_score



### Generators ###
def all_two_card_combinations_single_deck():
    combinations = list(itertools.combinations(bjo.base_deck, 2))
    for combination in combinations:
        yield combination


def all_three_card_combinations_single_deck():
    combinations = list(itertools.combinations(bjo.base_deck, 3))
    for combination in combinations:
        yield combination


"""
def test_combinations():
    object_list = [1, 2, 3, 4]
    combinations = list(itertools.combinations(object_list, 2))
    for combination in combinations:
        yield combination

count = 0

for value in all_two_card_combinations_single_deck():
    count += 1
    print(value, 'at count of: ', count)
"""