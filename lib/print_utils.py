""" 
File: print_utils.py
Author: Alexander Bulanov
"""

# Global Imports #
import msvcrt
import sys

# Local Imports #
from . import blackjack_game_objects as bjo

# Global-scope reference objects #
key_to_chip_default_bindings = {
    '1': 'White',
    '2': 'Pink',
    '3': 'Red',
    '4': 'Blue',
    '5': 'Green',
    '6': 'Black',
    '7': 'Purple',
    '8': 'Yellow',
    '9': 'Brown'
}

key_to_chip_decrement_bindings = {
    '!': 'White',
    '@': 'Pink',
    '#': 'Red',
    '$': 'Blue',
    '%': 'Green',
    '^': 'Black',
    '&': 'Purple',
    '*': 'Yellow',
    '(': 'Brown'
}

special_main_bet_key_bindings = {
    'v': 'view betting interface',
    'd': 'display player chip pool',
    'p': 'print current bet',
    'r': 'reset current bet',
    'f': 'finish current bet',
    's': 'skip betting',
    'g': 'get chips',
    'c': 'color up',
    'b': 'break down',
    'm': 'move seat',
    'a': 'add seat',
    'l': 'leave seat'
}

player_turn_core_actions_keybindings = {
    '1': 'stand',
    '2': 'hit',
    '3': 'double',
    '4': 'split',
    '5': 'surrender'
}

player_turn_special_actions_keybindings = {
    'v': 'view turn action options',
    'p': 'print current bet',
    'c': 'color up',
    'b': 'break down'
}

# Usage - print(f"Add seat {seat_selection_bindings[index]}")
seat_selection_bindings = {
    '1': '#1',
    '2': '#2',
    '3': '#3',
    '4': '#4',
    '5': '#5',
    '6': '#6',
    '7': '#7'
}

# Usage - print(f"Remove seat {seat_selection_bindings[index]}")
seat_deselection_bindings = {
    '!': '#1',
    '@': '#2',
    '#': '#3',
    '$': '#4',
    '%': '#5',
    '^': '#6',
    '&': '#7'
}

special_seat_selection_keybindings = {
    'v': 'view seat selection interface',
    'r': 'reset chosen seats',
    'c': 'confirm chosen seats'
}

def view_seat_selection_interface():
    print("Press the following number keys to select seats, symbol keys to deselect seats, and letter keys to execute special actions:")
    for seat_add_keybind, seat_name_to_add in seat_selection_bindings.items():
        print(f"{seat_add_keybind}: Add seat {seat_name_to_add}", end='')
        print_seat_selection_interface_padding()
        seat_remove_keybind = list(seat_deselection_bindings.keys())[int(seat_add_keybind)-1]
        seat_name_to_remove = seat_deselection_bindings[seat_remove_keybind]
        print(f"{seat_remove_keybind}: Remove seat {seat_name_to_remove}", end='')
        if len(list(special_seat_selection_keybindings.keys())) >= int(seat_add_keybind):
            print_seat_selection_interface_padding()
            special_seat_selection_keybind = list(special_seat_selection_keybindings.keys())[int(seat_add_keybind)-1]
            special_seat_selection_keybind_description = special_seat_selection_keybindings[special_seat_selection_keybind]
            print(f"{special_seat_selection_keybind}: {special_seat_selection_keybind_description}")
        else:
            print()

def print_seat_selection_interface_padding():
    for num in range(0, 4):
        print(" ", end='')

def print_betting_interface_padding(chip_color):
        padding_spaces = 14
        for char in str(bjo.chips[chip_color]):
            padding_spaces -= 1
        for char in chip_color:
            padding_spaces -= 1
        for num in range(0, padding_spaces):
            print(" ", end='')

def print_chip_bet_keybinding(chip_keybind, chip_color):
    if ((int(chip_keybind)-1) < 6):
        other_keybindings_list = list(special_main_bet_key_bindings.keys())
        # Print 6 keybindings in one column, then 6 more in the padded one to the right
        print_betting_interface_padding(chip_color)
        other_keybind_col_one = other_keybindings_list[int(chip_keybind)-1]
        print(f"{other_keybind_col_one}: {special_main_bet_key_bindings[other_keybind_col_one]}", end='')
        padding_spaces = 28
        other_keybinding_names = list(special_main_bet_key_bindings.values())
        other_keybinding_name = other_keybinding_names[int(chip_keybind)-1]
        #print(repr(other_keybinding_name))
        for char in other_keybinding_name:
            padding_spaces -= 1
        #print(padding_spaces, end='')
        for num in range(0, padding_spaces):
            print(" ", end='')
        other_keybind_col_two = other_keybindings_list[int(chip_keybind)-1+6]
        print(f"{other_keybind_col_two}: {special_main_bet_key_bindings[other_keybind_col_two]}")
    else:
        print("")

def view_chip_betting_interface():
    print("Press the following number keys to add chips, symbol keys to remove chips, and letter keys to execute special actions:")
    for chip_keybind, chip_color in key_to_chip_default_bindings.items():
        print(f"{chip_keybind}: +${bjo.chips[chip_color]} ({chip_color})", end='')
        print_betting_interface_padding(chip_color)
        chip_decrement_keybind = list(key_to_chip_decrement_bindings.keys())[int(chip_keybind)-1]
        print(f"{chip_decrement_keybind}: -${bjo.chips[chip_color]} ({chip_color})", end='')
        print_chip_bet_keybinding(chip_keybind, chip_color)


def view_game_launch_options(): # Todo AB: Implement
    pass


def view_side_bet_options_interface(): # Todo AB: Implement
    pass


def print_turn_action_option_interface_padding(action):
        padding_spaces = 13
        for char in action:
            padding_spaces -= 1
        for num in range(0, padding_spaces):
            print(" ", end='')

def view_player_turn_action_options():
    print("Press one of the following number or letter keys to choose a turn action:")
    for digit_key, action in player_turn_core_actions_keybindings.items():
        print(f"{digit_key}: {action}", end='')
        # Print padding, letter key and its meaning (4 special action keys available)
        if int(digit_key) < 5:
            print_turn_action_option_interface_padding(action)
            turn_action_special_keybind, turn_action_special_keybind_description = list(player_turn_special_actions_keybindings.items())[int(digit_key)-1]
            print(f"{turn_action_special_keybind}: {turn_action_special_keybind_description}")
    print("")