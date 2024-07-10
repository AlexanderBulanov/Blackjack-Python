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


"""
def square(x):
    return x*x

def square_and_cube(x):
    return x*x, x*x*x

def square_cube_and_quad(x):
    return x*x, x*x*x, x*x*x*x

x = 2
x_squared, x_cubed, x_quad = square_cube_and_quad(x)
print(f"Square of {x} is {x_squared}, cube of {x} is {x_cubed}, and quad of {x} is {x_quad}")
"""








#import lib.blackjack_game_objects as bjo
#import math


# Algo Flow
# 1. Pay out 1 Pink chip if bet is fractional
# 2. Pay out leftover non-Pink chips until bet is paid out

"""
player_chip_bet = dict.fromkeys(bjo.chip_names, 0)
player_chip_bet['Blue'] = 2
player_chip_bet['Green'] = 1

dealer_balance = dict.fromkeys(bjo.chip_names, 1000)

for chip_color, chip_count in player_chip_bet.items():
    dealer_balance[chip_color] += chip_count
"""





"""
remaining_payout = 13.5

if (type(remaining_payout) == float):
    print(f"Paying out 1 Pink chip for remaining bet of ${remaining_payout}")
    remaining_payout -= 1*2.5
    remaining_payout = int(remaining_payout)
    print(f"${remaining_payout} remaining to pay out")
if (remaining_payout != 0):
    for chip_name, chip_value in bjo.reverse_chips.items():
        if chip_name != 'Pink':
            remainder = remaining_payout % chip_value
            #print(remainder)
            if (remainder in range(0, remaining_payout)):
                num_of_chips = math.floor(remaining_payout/chip_value)
                print(f"Paying out {num_of_chips} {chip_name} chips for remaining bet of ${remaining_payout}")
                remaining_payout -= num_of_chips*chip_value
                if (remaining_payout == 0):
                    print(f"Bet fully paid out!")
                    break
                else:
                    print(f"${remaining_payout} remaining to pay out")
            else:
                pass
                #print(f"{chip_name} is too large of a unit to pay out this bet, trying a smaller chip")
else:
    print(f"Bet fully paid out!")
"""

"""
if type(remaining_payout) == int:
    for chip_name, chip_value in bjo.reverse_chips.items():
        #chip_name = 'Blue'
        #chip_value = bjo.chips[chip_name]
        remainder = remaining_payout % chip_value
        print(remainder)
        if (remainder in range(0, remaining_payout)):
            num_of_chips = math.floor(remaining_payout/chip_value)
            print(f"Paying out {num_of_chips} {chip_name} chips for remaining bet of ${remaining_payout}")
            remaining_payout -= num_of_chips*chip_value
            if (remaining_payout == 0):
                print(f"Bet fully paid out!")
                break
            else:
                print(f"Still need to pay out ${remaining_payout}")
        else:
            pass
            #print(f"{chip_name} is too large of a unit to pay out this bet, trying a smaller chip")
else:
    pass
"""