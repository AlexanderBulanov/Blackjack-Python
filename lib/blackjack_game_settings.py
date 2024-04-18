""" 
File: blackjack_game_settings.py
Author: Alexander Bulanov
"""

### Imports ###
import random

"""
def blackjack_preset_factory():
    # Generate preset for a blackjack game, given input variables/flags
"""

### Special Rules ###
# dealer_courtesy_rule - $2.5 chips can be bet only in pairs


### CASINO (DEFAULT) Game Settings ###
casino_num_of_decks = 6 # integers - 1/2/4/6/8
casino_min_bet = 5 # integers - $1/2/3/5/10/15/25/50/100
casino_max_bet = 100 # integers - 20*min_bet <= max_bet <= 100*min_bet
casino_blackjack_ratio = 3/2 # fractions - 6/5, 3/2

casino_deck_pen_percentage_bounds = {
    1: [50, 70],
    2: [55, 75],
    4: [60, 80],
    6: [65, 85],
    8: [70, 90]
}


# CASINO (DEFAULT) Game Settings Preset #
new_var = random.randrange(casino_deck_pen_percentage_bounds[casino_num_of_decks][0], 
                                        casino_deck_pen_percentage_bounds[casino_num_of_decks][1], 1)
                     
casino_game_preset = {
    'preset_name': ['casino'],
    'player_min': [1],
    'player_max': [7],
    'dealer_type': ['default'], # fixed dealer; "resolves" players left-to-right /w self going last
    'card_visibility': ['default'], # all cards face-up except for dealer's 2nd
    'buy-in_mode': ['default'], # any chip amount OK, as long as it is 20x the min_bet
    'round_payout': ['default'], # 1:1 on non-blackjack wins, pays casino_blackjack_ratio on wins
    'game_payout': ['default'], # all players' chips converted into equivalent $
    'num_of_decks': [casino_num_of_decks],
    'card_storage': ['shoe'],
    'pen_percentage': [new_var],
    'min_bet': [casino_min_bet],
    'max_bet': [casino_max_bet],
    'blackjack_ratio': [casino_blackjack_ratio],
    'payout_rounding': ['0.5', 'up'], # round to nearest $0.50, up at $x.25 and $x.75
    'seventeen_rule': ['S17'],
    'doubling_rules': ['DA2', 'DAS'],
    'split_rules': ['SP4', 'NRSA'],
    'surrender_options': ['LS'],
    'join_restrictions': ['NMSE']
}


"""
### HOME Game Settings ###
home_num_of_decks = 6 # integers - 1, 2, 4, 6, 8
home_min_bet = 1 # recommended minimum
home_max_bet = 10 # recommended maximums - 5, 10
home_blackjack_ratio = 3/2 # recommended ratio

home_deck_pen_percentage_bounds = {
    1: [50, 70],
    2: [55, 75],
    4: [60, 80],
    6: [65, 85],
    8: [70, 90]
}

# HOME Game Settings Preset #
home_game_preset = {
    'preset_name': ['home'],
    'player_min': [2], # at least 2 players needed to run 'home' game
    'player_max': [7],
    'dealer_type': ['rotating'],
    'card_visibility': ['default'],
    'buy-in_mode': [['flat', 20]], # $20 gets turned into $80 in chips (1/4th purchasing power) for better play experience
    'round_payout': ['default'],
    'game_payout': ['fractional'], # end-of-game (fractional) chip totals pay out 25%
    'num_of_decks': [home_num_of_decks],
    'card_storage': ['shoe'],
    'pen_percentage': [random.randrange(home_deck_pen_percentage_bounds[home_num_of_decks][0], home_deck_pen_percentage_bounds[home_num_of_decks][1], 1)],
    'min_bet': [home_min_bet],
    'max_bet': [home_max_bet],
    'blackjack_ratio': [home_blackjack_ratio],
    'payout_rounding': ['0.5', 'up'], # round to nearest $0.50, up at $x.25 and $x.75
    'seventeen_rule': ['S17'],
    'doubling_rules': ['DA2', 'DAS'],
    'split_rules': ['SP4', 'NRSA'],
    'surrender_options': ['None'],
    'join_restrictions': ['None']
}


### CUSTOM Game Settings ###
custom_num_of_decks = 6 # integers - 1/2/4/6/8
custom_min_bet = 5 # integers - $1/2/3/5/10/15/25/50/100
custom_max_bet = 100 # integers - 20*min_bet <= max_bet <= 100*min_bet
custom_blackjack_ratio = 3/2 # fractions - 6/5, 3/2

custom_deck_pen_percentage_bounds = {
    1: [50, 70],
    2: [55, 75],
    4: [60, 80],
    6: [65, 85],
    8: [70, 90]
}

# CUSTOM Game Settings Preset #
custom_game_preset = {
    'preset_name': ['casino', 'home', 'custom'],
    'player_min': [1, 2],
    'player_max': [7],
    'dealer_type': ['default', 'rotating', 'none'],
    'card_visibility': ['default', 'second-down', 'all-up'],
    'buy-in_mode': ['default', 'flat', 'phantom'],
    'round_payout': ['default', 'highest-totals-take-all'],
    'game_payout': ['default', 'fractional', 'phantom'],
    'num_of_decks': [custom_num_of_decks],
    'card_storage': ['shoe', 'csm'],
    'pen_percentage': [random.randrange(custom_deck_pen_percentage_bounds[custom_num_of_decks][0], custom_deck_pen_percentage_bounds[custom_num_of_decks][1], 1)],
    'min_bet': [custom_min_bet],
    'max_bet': [custom_max_bet],
    'blackjack_ratio': [custom_blackjack_ratio],
    'payout_rounding': [['0.5', 'down'], ['0.5', 'up']], # round to nearest $0.50, up at $x.25 and $x.75
    'seventeen_rule': ['S17' 'H17'],
    'doubling_rules': [['DA2', 'D9', 'D10'], ['DAS', 'NDAS']],
    'split_rules': [['SP2', 'SP4'], ['RSA', 'NRSA']],
    'surrender_options': ['None', 'ES', 'ES10', 'LS'],
    'join_restrictions': ['None', 'NMSE']
}
"""