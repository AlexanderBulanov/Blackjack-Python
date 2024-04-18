""" 
File: score_test.py
Author: Alexander Bulanov
"""

### Imports ###
import lib.blackjack_game_logic as bjl


### Explicit Testing - Edge Cases (Hands /w Aces) for a 1D Blackjack ###
## One-Card Hands ##
def test_hand_score_ace_expect_eleven():
    test_hand = ['AS']
    result = bjl.highest_hand_score(test_hand)
    assert result == 11
    print(result)

## Two-Card Hands ##
def test_hand_score_ace_jack_expect_blackjack():
    test_hand = ['AH', 'JC']
    result = bjl.highest_hand_score(test_hand)
    assert result == 21
    print(result)

def test_hand_score_eight_ace_expect_nineteen():
    test_hand = ['8H', 'AC']
    result = bjl.highest_hand_score(test_hand)
    assert result == 19
    print(result)

def test_hand_score_double_ace_expect_twelve():
    test_hand = ['AH', 'AC']
    result = bjl.highest_hand_score(test_hand)
    assert result == 12
    print(result)


## Three-Card Hands ##
def test_hand_score_three_ace_six_expect_twenty():
    test_hand = ['3D', 'AS', '6S']
    result = bjl.highest_hand_score(test_hand)
    assert result == 20
    print(result)

def test_hand_score_eight_nine_ace_expect_eighteen():
    test_hand = ['8C', '9S', 'AH']
    result = bjl.highest_hand_score(test_hand)
    assert result == 18
    print(result)

def test_hand_score_triple_ace_expect_thirteen():
    test_hand = ['AH', 'AC', 'AS']
    result = bjl.highest_hand_score(test_hand)
    assert result == 13
    print(result)


## Four-Card Hands ##
# Non-Bust Hands #
def test_hand_score_seven_two_double_ace_expect_blackjack():
    test_hand = ['7D', '2S', 'AS', 'AD']
    result = bjl.highest_hand_score(test_hand)
    assert result == 21
    print(result)

def test_hand_score_ace_five_four_two_expect_twelve():
    test_hand = ['AH', '5H', '4C', '2D']
    result = bjl.highest_hand_score(test_hand)
    assert result == 12
    print(result)

def test_hand_score_quad_ace_expect_fourteen():
    test_hand = ['AH', 'AC', 'AS', 'AD']
    result = bjl.highest_hand_score(test_hand)
    assert result == 14
    print(result)

# Bust Hands #
def test_hand_score_double_ace_jack_queen_expect_bust():
    test_hand = ['AH', 'AC', 'JH', 'QD']
    result = bjl.highest_hand_score(test_hand)
    assert result == -1
    print(result)

# Hands that exceed Blackjack and aren't counted past 21 due to "having won" at the time; hand value adds up to Blackjack #
def test_hand_score_jack_ace_ace_queen_expect_bust():
    test_hand = ['JD', 'AS', 'AC', 'QH']
    result = bjl.highest_hand_score(test_hand)
    assert result == 21
    print(result)

def test_hand_score_jack_queen_ace_ace_expect_bust():
    test_hand = ['JD', 'QH', 'AS', 'AC']
    result = bjl.highest_hand_score(test_hand)
    assert result == 21
    print(result)


## Five-Card Hands ##
def test_hand_score_three_two_ace_four_ace_expect_blackjack():
    test_hand = ['3H', '2D', 'AC', '4D', 'AH']
    result = bjl.highest_hand_score(test_hand)
    assert result == 21
    print(result)

def test_hand_score_quad_twos_ace_expect_nineteen():
    test_hand = ['2H', '2C', '2D', '2S', 'AD']
    result = bjl.highest_hand_score(test_hand)
    assert result == 19
    print(result)

def test_hand_score_triple_threes_ace_jack_expect_twenty():
    test_hand = ['3D', '3H', '3C', 'AS', 'JS']
    result = bjl.highest_hand_score(test_hand)
    assert result == 20
    print(result)



### Explicit Testing - Select Internal Cases (Hands w/o Aces) for a 1D Blackjack ###
## One-Card Hands ##
def test_hand_score_seven_expect_seven():
    test_hand = ['7D']
    result = bjl.highest_hand_score(test_hand)
    assert result == 7
    print(result)

def test_hand_score_queen_expect_ten():
    test_hand = ['QH']
    result = bjl.highest_hand_score(test_hand)
    assert result == 10
    print(result)


## Two-Card Hands ##
def test_hand_score_seven_eight_expect_fifteen():
    test_hand = ['7H', '8C']
    result = bjl.highest_hand_score(test_hand)
    assert result == 15
    print(result)

def test_hand_score_four_nine_expect_thirteen():
    test_hand = ['4D', '9S']
    result = bjl.highest_hand_score(test_hand)
    assert result == 13
    print(result)

def test_hand_score_king_queen_expect_twenty():
    test_hand = ['KH', 'QD']
    result = bjl.highest_hand_score(test_hand)
    assert result == 20
    print(result)


"""
### Implicit Testing - General Cases for a 1D Blackjack ###
## Two-Card Hands ##
def test_all_two_card_hands_scored_correctly_single_deck():
    list_of_all_two_card_combinations_single_deck = bjl.all_two_card_combinations_single_deck()
    for card_pair in list_of_all_two_card_combinations_single_deck:
        # Using highest_hand_score() to calculate two-card hand value
        score_result = bjl.highest_hand_score(card_pair)
        # Setting up variables to manually calculate two-card hand value for test comparison
        expected_two_card_hand_value = 0
        key_first_card = card_pair[0][:-1]
        key_second_card = card_pair[1][:-1]
        high_value_first_card = bjo.cards[key_first_card][-1]
        low_value_second_card = bjo.cards[key_second_card][0] # same as high_value_second_card for every card but Ace (equal to 1)
        high_value_second_card = bjo.cards[key_second_card][-1] # same as low_value_second_card for every card but Ace (equal to 11)
        # Manually calculating two-card hand value for test comparison
        expected_two_card_hand_value += high_value_first_card
        if ((expected_two_card_hand_value + high_value_second_card) > 21):
            expected_two_card_hand_value += low_value_second_card
        else:
            expected_two_card_hand_value += high_value_second_card
        # Testing that highest_hand_score() output matches expected value
        assert score_result == expected_two_card_hand_value


## Three-Card Hands ##
def test_all_three_card_hands_scored_correctly_single_deck():
    list_of_all_three_card_combinations_single_deck = bjl.all_three_card_combinations_single_deck()
    for card_triple in list_of_all_three_card_combinations_single_deck:
        # Using highest_hand_score() to calculate three-card hand value
        score_result = bjl.highest_hand_score(card_triple)
        # Setting up variables to manually calculate three-card hand value for test comparison
        expected_three_card_hand_value = 0
        key_first_card = card_triple[0][:-1]
        key_second_card = card_triple[1][:-1]
        key_third_card = card_triple[2][:-1]
        high_value_first_card = bjo.cards[key_first_card][-1]
        low_value_second_card = bjo.cards[key_second_card][0] # same as high_value_second_card for every card but Ace (equal to 1)
        high_value_second_card = bjo.cards[key_second_card][-1] # same as low_value_second_card for every card but Ace (equal to 11)
        low_value_third_card = bjo.cards[key_third_card][0] # same as high_value_third_card for every card but Ace (equal to 1)
        high_value_third_card = bjo.cards[key_third_card][-1] # same as low_value_third_card for every card but Ace (equal to 11)
        # Manually calculating three-card hand value for test comparison
        # Adding second card #
        expected_three_card_hand_value += high_value_first_card
        if ((expected_three_card_hand_value + high_value_second_card) > 21):
            expected_three_card_hand_value += low_value_second_card
        else:
            expected_three_card_hand_value += high_value_second_card
        print('Sum total for first two cards is: ',expected_three_card_hand_value)
        # Adding third card #
        if (((expected_three_card_hand_value + high_value_third_card) > 21) and
            ((expected_three_card_hand_value + low_value_third_card) > 21) and
            ((expected_three_card_hand_value != 21)) and # third card isn't scored by highest_hand_score() if first two result in Blackjack
            (((key_first_card != 'A') and (key_second_card != 'A')))):
            #print('Current hand is: ',card_triple, ' and it has value of ',bjl.highest_hand_score(card_triple))
            #print ('Card keys are: ',key_first_card,key_second_card,key_third_card)
            assert score_result == -1
        elif (((expected_three_card_hand_value + high_value_third_card) > 21) and
            ((expected_three_card_hand_value + low_value_third_card) > 21) and
            ((expected_three_card_hand_value != 21)) and # third card isn't scored by highest_hand_score() if first two result in Blackjack
            (((key_first_card == 'A') or (key_second_card == 'A')))):
            #print('Current hand is: ',card_triple, ' and it has value of ',bjl.highest_hand_score(card_triple))
            #print ('Card keys are: ',key_first_card,key_second_card,key_third_card)
            expected_three_card_hand_value += low_value_third_card
            expected_three_card_hand_value -= 10
            assert score_result == expected_three_card_hand_value
        elif (((expected_three_card_hand_value + high_value_third_card) > 21) and
            ((expected_three_card_hand_value + low_value_third_card) <= 21)):
            expected_three_card_hand_value += low_value_third_card
            assert score_result == expected_three_card_hand_value
        elif ((expected_three_card_hand_value + high_value_third_card) < 21):
            expected_three_card_hand_value += high_value_third_card
            assert score_result == expected_three_card_hand_value
"""