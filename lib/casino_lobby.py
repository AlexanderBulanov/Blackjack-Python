""" 
File: casino_lobby.py
Author: Alexander Bulanov
"""

# Global Imports #
import msvcrt
import sys

# Local Imports #
from . import blackjack_fsm as bjfsm
from . import blackjack_game_objects as bjo
from . import print_utils as prutils


#print(f"Welcome to Blackjack! Please select game launch options from the ones listed below.")
#prutils.view_game_launch_options()

# 1. Prompt administrator for table setup:
# 1a. Default preset (6D, $1-$100, 3/2, 'H17', 'NS', 'DA2', 'DAS', 'SP4', 'Rank', 'RSA', 'Perfect Pairs', 'NMSE') (/w overview of its details shown to admin)
# 1b. Load a JSON preset (/w overview of its details shown to admin)
# 1c. Manually select game launch options:
#       num_of_decks, (1, 2, 4, 6, 8)
#       min_bet, (1-100; at least 10x smaller than max_bet)
#       max_bet, (100-10000; at least 10x bigger than min_bet)
#       blackjack_ratio, (3/2, 6/5)
#       seventeen_rule, ('S17', 'H17')
#       surrender_rule, ('NS', 'ES', 'ES10', 'LS')
#       doubling_rule, ('DA2', 'D9', 'D10')
#       double_after_split_rule, ('DAS', 'NDAS')
#       splitting_rule, ('SP2', 'SP4')
#       split_10s_rule, ('Value', 'Rank')
#       ace_resplit_rule, ('RSA', , 'RSA3', 'NRSA')
#       table_side_bet_names (table_side_bet_limits, table_side_bet_payout tables - both autopopulated from names for num_of_decks > 1)
#       joining_restriction (None, 'NMSE')
# 2. Ask administrator if they'd like to save manually chosen game launch options 
# 3. Instantiate Blackjack State Machine (renamed as blackjack_table.py) with provided game launch options


# 1. Parse JSON file /w table preset/ruleset
# 2. Spin up an instance of Blackjack state machine with provided preset/ruleset
num_of_decks = 1
BlackjackSM = bjfsm.BlackjackStateMachine(num_of_decks)
BlackjackSM.run()