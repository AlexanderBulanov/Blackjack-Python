""" 
File: main.py
Author: Alexander Bulanov
"""

### Global Imports ###


### Local Imports ###
import lib.blackjack_fsm as bjfsm
import lib.blackjack_players as bjp

### Main Code ###
PlayerAlex = bjp.Player.create_new_player('Alex')
PlayerAlex.print_player_stats()


BlackjackSM = bjfsm.BlackjackStateMachine(1)
BlackjackSM.run()
