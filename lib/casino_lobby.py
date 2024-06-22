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


print(f"Welcome to Blackjack! Please select game launch options from the ones listed below.")
prutils.view_game_launch_options()

# Somehow store game launch options

num_of_decks = 1
BlackjackSM = bjfsm.BlackjackStateMachine(num_of_decks)
BlackjackSM.run()