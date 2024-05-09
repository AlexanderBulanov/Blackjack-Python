""" 
File: main.py
Author: Alexander Bulanov
"""

### Global Imports ###


### Local Imports ###
import lib.blackjack_fsm as bjfsm

### Main Code ###
BlackjackSM = bjfsm.BlackjackStateMachine(1)
BlackjackSM.run()