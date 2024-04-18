""" 
File: generator_test.py
Author: Alexander Bulanov
"""

### Imports ###
import lib.blackjack_game_objects as bjo
import lib.blackjack_game_logic as bjl


### Implicit Testing - General Cases ###
def test_all_two_card_combinations_created_correctly():
    # Create a dictionary of all 52 cards as keys, with values indicating how many times they have each been generated
    card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
    # Iterate over every generated card pair, updating number of times each card has been used in a combination
    for card in card_occurrence_counts:
        for card_pair in bjl.all_two_card_combinations_single_deck():
            if ((card_pair[0] == card) or (card_pair[1] == card)):
                card_occurrence_counts[card] += 1
    # Iterate over counts of how many times each card has been used in a combination (expected value is 51 for each)
    for card in card_occurrence_counts:
        #print(card, 'has been used', card_occurrence_counts[card], 'times; 51 expected')
        assert card_occurrence_counts[card] == 51 # 51 is equivalent to 1 Choose 1 * 51 Choose 1


def test_all_three_card_combinations_created_correctly():
    # Create a dictionary of all 52 cards as keys, with values indicating how many times they have each been generated
    card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
    # Iterate over every generated card pair, updating number of times each card has been used in a combination
    for card in card_occurrence_counts:
        for card_triple in bjl.all_three_card_combinations_single_deck():
            if ((card_triple[0] == card) or (card_triple[1] == card) or (card_triple[2] == card)):
                card_occurrence_counts[card] += 1
    # Iterate over counts of how many times each card has been used in a combination (expected value is 51 for each)
    for card in card_occurrence_counts:
        #print(card, 'has been used', card_occurrence_counts[card], 'times; 51 expected')
        assert card_occurrence_counts[card] == 1275 #1275 is equivalent to 1 Choose 1 * 51 Choose 2