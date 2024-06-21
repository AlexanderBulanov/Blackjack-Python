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
    '9': 'Brown',
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
    '(': 'Brown',
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
    'l': 'leave seat',
}

def print_betting_interface_padding(chip_color):
        padding_spaces = 14
        for char in str(bjo.chips[chip_color]):
            padding_spaces -= 1
        for char in chip_color:
            padding_spaces -= 1
        for num in range(0, padding_spaces):
            print(" ", end='')

def print_letter_keybinding(chip_keybind, chip_color):
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
        print_letter_keybinding(chip_keybind, chip_color)





def view_side_bet_options_interface():
    pass