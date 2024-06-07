""" 
File: blackjack_fsm_test.py
Author: Alexander Bulanov
"""

# Global Imports
from enum import Enum
import pytest

# Local Imports #
import lib.blackjack_fsm as bjfsm
import lib.blackjack_game_settings as bjs
import lib.blackjack_game_objects as bjo


class Test_WAITING:
    def test_blackjack_state_machine_beginning_state_is_WAITING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        assert test_machine.state == bjfsm.GameState.WAITING

    def test_blackjack_state_machine_transitions_to_STARTING_from_WAITING_after_one_player_starts_game(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Test
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        assert test_machine.state == bjfsm.GameState.STARTING

    def test_first_player_Alex_correctly_assigned_to_seat_2(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Test
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        assert test_machine.seated_players[2].name == 'Alex'

    def test_second_player_Jim_tries_to_sit_in_Alex_occupied_seat_2_then_chooses_seat_3_is_seated_correctly(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Test
        simulated_input_values = ['Alex', '2', 'Jim', '2', '3']
        iterable_simulated_input_values = iter(simulated_input_values)
        simulated_char_values = [b'p', b's']
        iterable_simulated_char_values = iter(simulated_char_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_values))
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        assert test_machine.seated_players[2].name == 'Alex'
        assert test_machine.seated_players[3].name == 'Jim'
        assert test_machine.state == bjfsm.GameState.STARTING

    def test_Alex_Jim_John_correctly_seated_in_seats_2_3_7_respectively(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Test
        simulated_input_values = ['Alex', '2', 'Jim', '2', '3', 'John', '7']
        iterable_simulated_input_values = iter(simulated_input_values)
        simulated_char_values = [b'p', b'p', b's']
        iterable_simulated_char_values = iter(simulated_char_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_values))
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        assert test_machine.seated_players[2].name == 'Alex'
        assert test_machine.seated_players[3].name == 'Jim'
        assert test_machine.seated_players[7].name == 'John'
        assert test_machine.state == bjfsm.GameState.STARTING
    
    def test_all_seats_assigned_correctly_to_seven_joined_players(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Test
        simulated_input_values = ['Alex', '2', 'Jim', '3', 'John', '7', 'Mike', '1', 'Kim', '4', 'Jane', '5', 'Bob']
        iterable_simulated_input_values = iter(simulated_input_values)
        simulated_char_values = [b'p'] * 6
        iterable_simulated_char_values = iter(simulated_char_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_values))
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        assert test_machine.seated_players[1].name == 'Mike'
        assert test_machine.seated_players[2].name == 'Alex'
        assert test_machine.seated_players[3].name == 'Jim'
        assert test_machine.seated_players[4].name == 'Kim'
        assert test_machine.seated_players[5].name == 'Jane'
        assert test_machine.seated_players[6].name == 'Bob'
        assert test_machine.seated_players[7].name == 'John'
        assert test_machine.state == bjfsm.GameState.STARTING

class Test_STARTING:
    def test_blackjack_state_machine_transitions_to_SHUFFLING_from_STARTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        # Test
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        assert test_machine.state == bjfsm.GameState.SHUFFLING
    
    def test_only_joined_player_Alex_in_seat_2_set_to_active_in_STARTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        # Test
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        assert test_machine.seated_players[2].name == 'Alex'
        assert test_machine.active_player == test_machine.seated_players[2]

    def test_players_Alex_and_Ahmed_join_table_seats_2_and_1_Ahmed_in_leftmost_seat_set_to_active_in_STARTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2', 'Ahmed', '1']
        iterable_simulated_input_values = iter(simulated_input_values)
        simulated_char_values = [b'p', b's']
        iterable_simulated_char_values = iter(simulated_char_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_values))
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        # Test
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        assert test_machine.seated_players[1].name == 'Ahmed'
        assert test_machine.seated_players[2].name == 'Alex'
        assert test_machine.active_player == test_machine.seated_players[1]

    def test_only_joined_player_Alex_added_to_known_players_in_STARTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING and transitions to STARTING
        # Test
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        assert test_machine.seated_players[2].name == 'Alex'
        assert len(test_machine.known_players) == 1
        assert test_machine.seated_players[2] in test_machine.known_players

    def test_both_players_Alex_in_seat_2_and_Ahmed_in_seat_1_added_to_known_players_in_STARTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2', 'Ahmed', '1']
        iterable_simulated_input_values = iter(simulated_input_values)
        simulated_char_values = [b'p', b's']
        iterable_simulated_char_values = iter(simulated_char_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_values))
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        # Test
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        assert test_machine.seated_players[1].name == 'Ahmed'
        assert test_machine.seated_players[2].name == 'Alex'
        assert len(test_machine.known_players) == 2
        assert test_machine.seated_players[1] in test_machine.known_players
        assert test_machine.seated_players[2] in test_machine.known_players

    """
    def test_joined_known_player_not_readded_to_list_of_known_players_in_STARTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        # Test
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        # WRITE TEST TO VERIFY NEW PLAYER OBJECT ISN'T CREATED WHEN PLAYER REJOINS TABLE AFTER LEAVING
        ### Test Code Here ###
    """

class Test_SHUFFLING:
    def test_blackjack_state_machine_transitions_to_BETTING_from_SHUFFLING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        # Test
        test_machine.step() # executes shuffle_cut_and_burn() in SHUFFLING and transitions to BETTING
        assert test_machine.state == bjfsm.GameState.BETTING

    def test_starting_single_deck_shoe_is_shuffle_cut_and_burned_correctly_at_randomly_chosen_pen_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.step() # executes shuffle_cut_and_burn() in SHUFFLING and transitions to BETTING
        ## Shoe Integrity Test ##
        # Verify deck size and pen percentage is in-bounds for a single deck shoe
        assert len(test_machine.shoe) == 1+52*1
        assert test_machine.pen in range(50, 71)
        # Verify cut cards are present and are placed correctly in-bounds for a single deck shoe
        assert 'front_cut_card' in test_machine.shoe[26:37]
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 1 copy of each non-cut card across shoe and discard, for a single deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 1

    def test_starting_eight_deck_shoe_is_shuffle_cut_and_burned_correctly_at_randomly_chosen_pen_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 8
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.step() # executes shuffle_cut_and_burn() in SHUFFLING and transitions to BETTING
        ## Shoe Integrity Test ##
        # Verify deck size and pen percentage is in-bounds for an eight-deck shoe
        assert len(test_machine.shoe) == 1+52*8
        assert test_machine.pen in range(70, 91)
        # Verify cut cards are present and are placed correctly in-bounds for an eight-deck shoe
        assert 'front_cut_card' in test_machine.shoe[291:375]
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 8 copies of each non-cut card across shoe and discard, for an eight-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 8

    def test_one_deck_shoe_is_shuffle_cut_and_burned_correctly_at_min_pen_of_50_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 1
        min_cut_percentage_one_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][0]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_one_deck_shoe) # manually executes SHUFFLING /w 50% pen
        ## Shoe Integrity Test ##
        # Verify deck size and minimum (50%) pen percentage for a one-deck shoe
        assert len(test_machine.shoe) == 1+52*1
        assert test_machine.pen == 50
        # Verify cut cards are present and are placed correctly at minimum (50%) pen for a one-deck shoe
        assert test_machine.shoe[26] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 1 copy of each non-cut card across shoe and discard, for a one-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 1

    def test_one_deck_shoe_is_shuffle_cut_and_burned_correctly_at_max_pen_of_70_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 1
        min_cut_percentage_one_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][1]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_one_deck_shoe) # manually execute SHUFFLING /w 70% pen
        ## Shoe Integrity Test ##
        # Verify deck size and maximum (70%) pen percentage for a one-deck shoe
        assert len(test_machine.shoe) == 1+52*1
        assert test_machine.pen == 70
        # Verify cut cards are present and are placed correctly at maximum (70%) pen for a one-deck shoe
        assert test_machine.shoe[36] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 1 copy of each non-cut card across shoe and discard, for a one-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 1

    def test_two_deck_shoe_is_shuffle_cut_and_burned_correctly_at_min_pen_of_55_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 2
        min_cut_percentage_two_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][0]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_two_deck_shoe) # manually execute SHUFFLING /w 55% pen
        ## Shoe Integrity Test ##
        # Verify deck size and minimum (55%) pen percentage for a two-deck shoe
        assert len(test_machine.shoe) == 1+52*2
        assert test_machine.pen == 55
        # Verify cut cards are present and are placed correctly at minimum (55%) pen for a two-deck shoe
        assert test_machine.shoe[57] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 2 copies of each non-cut card across shoe and discard, for a two-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1   
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 2

    def test_two_deck_shoe_is_shuffle_cut_and_burned_correctly_at_max_pen_of_75_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 2
        min_cut_percentage_two_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][1]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_two_deck_shoe) # manually execute SHUFFLING /w 75% pen
        ## Shoe Integrity Test ##
        # Verify deck size and maximum (75%) pen percentage for a two-deck shoe
        assert len(test_machine.shoe) == 1+52*2
        assert test_machine.pen == 75
        # Verify cut cards are present and are placed correctly at maximum (75%) pen for a two-deck shoe
        assert test_machine.shoe[78] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 2 copies of each non-cut card across shoe and discard, for a two-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 2

    def test_four_deck_shoe_is_shuffle_cut_and_burned_correctly_at_min_pen_of_60_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 4
        min_cut_percentage_four_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][0]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_four_deck_shoe) # manually execute SHUFFLING /w 60% pen
        ## Shoe Integrity Test ##
        # Verify deck size and minimum (60%) pen percentage for a four-deck shoe
        assert len(test_machine.shoe) == 1+52*4
        assert test_machine.pen == 60
        # Verify cut cards are present and are placed correctly at minimum (60%) pen for a four-deck shoe
        assert test_machine.shoe[124] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 4 copies of each non-cut card across shoe and discard, for a four-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 4

    def test_four_deck_shoe_is_shuffle_cut_and_burned_correctly_at_max_pen_of_80_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 4
        min_cut_percentage_four_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][1]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_four_deck_shoe) # manually execute SHUFFLING /w 80% pen
        ## Shoe Integrity Test ##
        # Verify deck size and maximum (80%) pen percentage for a four-deck shoe
        assert len(test_machine.shoe) == 1+52*4
        assert test_machine.pen == 80
        # Verify cut cards are present and are placed correctly at maximum (80%) pen for a four-deck shoe
        assert test_machine.shoe[166] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 4 copies of each non-cut card across shoe and discard, for a four-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 4

    def test_six_deck_shoe_is_shuffle_cut_and_burned_correctly_at_min_pen_of_65_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 6
        min_cut_percentage_six_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][0]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_six_deck_shoe) # manually execute SHUFFLING /w 65% pen
        ## Shoe Integrity Test ##
        # Verify deck size and minimum (65%) pen percentage for a six-deck shoe
        assert len(test_machine.shoe) == 1+52*6
        assert test_machine.pen == 65
        # Verify cut cards are present and are placed correctly at minimum (65%) pen for a six-deck shoe
        assert test_machine.shoe[202] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 6 copies of each non-cut card across shoe and discard, for a six-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 6

    def test_six_deck_shoe_is_shuffle_cut_and_burned_correctly_at_max_pen_of_85_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 6
        min_cut_percentage_six_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][1]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_six_deck_shoe) # manually execute SHUFFLING /w 85% pen
        ## Shoe Integrity Test ##
        # Verify deck size and maximum (85%) pen percentage for a six-deck shoe
        assert len(test_machine.shoe) == 1+52*6
        assert test_machine.pen == 85
        # Verify cut cards are present and are placed correctly at maximum (85%) pen for a six-deck shoe
        assert test_machine.shoe[265] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 6 copies of each non-cut card across shoe and discard, for a six-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 6

    def test_eight_deck_shoe_is_shuffle_cut_and_burned_correctly_at_min_pen_of_70_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 8
        min_cut_percentage_eight_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][0]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_eight_deck_shoe) # manually execute SHUFFLING /w 70% pen
        ## Shoe Integrity Test ##
        # Verify deck size and minimum (70%) pen percentage for an eight-deck shoe
        assert len(test_machine.shoe) == 1+52*8
        assert test_machine.pen == 70
        # Verify cut cards are present and are placed correctly at minimum (70%) pen for an eight-deck shoe
        assert test_machine.shoe[291] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 8 copies of each non-cut card across shoe and discard, for an eight-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 8

    def test_eight_deck_shoe_is_shuffle_cut_and_burned_correctly_at_max_pen_of_90_percent_in_SHUFFLING(self, monkeypatch):
        ## Setup ##
        num_of_decks = 8
        min_cut_percentage_eight_deck_shoe = bjs.casino_deck_pen_percentage_bounds[num_of_decks][1]
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.shuffle_cut_and_burn(min_cut_percentage_eight_deck_shoe) # manually execute SHUFFLING /w 90% pen
        ## Shoe Integrity Test ##
        # Verify deck size and maximum (90%) pen percentage for an eight-deck shoe
        assert len(test_machine.shoe) == 1+52*8
        assert test_machine.pen == 90
        # Verify cut cards are present and are placed correctly at maximum (90%) pen for an eight-deck shoe
        assert test_machine.shoe[374] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 8 copies of each non-cut card across shoe and discard, for an eight-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        card_occurrence_counts[test_machine.discard[0]] += 1
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
            assert card_occurrence_counts[card] == 8

class Test_BETTING:
    def test_blackjack_state_machine_transitions_to_DEALING_from_BETTING(self, monkeypatch):
        # Setup
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        simulated_input_values = ['Alex', '2']
        iterable_simulated_input_values = iter(simulated_input_values)
        monkeypatch.setattr('builtins.input', lambda _: next(iterable_simulated_input_values))
        monkeypatch.setattr('msvcrt.getch', lambda: b's')
        test_machine.step() # executes wait_for_players_to_join() in WAITING and transitions to STARTING
        test_machine.step() # executes start_game() in STARTING and transitions to SHUFFLING
        test_machine.step() # executes shuffle_cut_and_burn() in SHUFFLING and transitions to BETTING
        # Test
        #simulated_char_inputs = [b'1', b'3', b'4', b'5', b'f']
        simulated_char_inputs = [b'1', b'f'] # provides a bet of 1 White chip
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
        test_machine.step() # executes get_all_players_bets() in BETTING and transitions to DEALING
        assert test_machine.state == bjfsm.GameState.DEALING

    def test_single_player_betting_two_pink_chips_continues_to_DEALING(self):
        pass

    def test_betting_fifty_one_white_chips_out_of_fifty_in_chip_pool_makes_for_a_fifty_dollar_bet(self, monkeypatch):
        pass

    def test_chip_pool_balance_plus_main_bet_amount_adds_to_five_hundred_for_template_player_after_BETTING(self, monkeypatch):
        pass

    def test_one_of_each_chip_placed_by_player_stored_correctly_at_table_seat(self, monkeypatch):
        pass

    
class Test_DEALING:
    def test_blackjack_state_machine_transitions_to_INITIAL_SCORING_from_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        test_machine.step() # Todo AB: handle BETTING state properly instead of just skipping over it
        test_machine.step() # executes deal() in DEALING
        assert test_machine.state == bjfsm.GameState.INITIAL_SCORING

    def test_first_player_has_one_hand_dealt_in_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # executes shuffle_cut_and_burn(None) in SHUFFLING
        test_machine.step() # Todo AB: handle BETTING state properly instead of just skipping over it
        test_machine.step() # executes deal() in DEALING
        assert len(test_machine.joined_players[2].current_hands) == 1 # BlackjackStateMachine currently manually sets up 1 player at table seat 2

    def test_dealer_has_one_hand_dealt_in_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # executes shuffle_cut_and_burn(None) in SHUFFLING
        test_machine.step() # Todo AB: handle BETTING state properly instead of just skipping over it
        test_machine.step() # executes deal() in DEALING
        assert len(test_machine.dealer.current_hands) == 1

    def test_one_deck_shoe_has_49_cards_left_after_one_player_and_one_dealer_are_dealt_hands_in_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # executes shuffle_cut_and_burn(None) in SHUFFLING
        test_machine.step() # Todo AB: handle BETTING state properly instead of just skipping over it
        test_machine.step() # executes deal() in DEALING
        assert len(test_machine.shoe) == 49


class TestNaturalBlackjacks_INITIAL_SCORING:
    def test_dealer_face_up_card_ace_has_blackjack_first_player_with_blackjack_hand_pushes_correctly_single_deck(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        # Manually execute shuffle_cut_and_burn(), burning '8H'
        test_machine.shuffle_cut_and_burn(None)
        test_machine.shoe.extend(test_machine.discard)
        test_machine.discard.clear()
        test_machine.discard.extend([test_machine.shoe.pop(test_machine.shoe.index('8H'))])
        assert ('8H' not in test_machine.shoe) and ('8H' in test_machine.discard)
        # Manually assign a bet of '2 White' with value of $2 to first player
        first_player = test_machine.joined_players[0]
        first_player_bet_string = '2 White, 1 Blue'
        alternate_bet_string = '112'


        first_player.add_primary_bet(player_hand, first_player_bet_string)



        first_player.current_primary_bets.append(first_player_bet_string.split(', '))
        first_player.current_primary_bet_values.append(2*1 + 1*5)
        first_player.White -= 2
        first_player.Blue -= 1
        # Manually deal a blackjack hand to first player
        player_hand = ['QD', 'AH']
        test_machine.shoe.pop(test_machine.shoe.index('QD'))
        test_machine.shoe.pop(test_machine.shoe.index('AH'))
        first_player.current_hands.append(player_hand)
        # Manually deal a blackjack hand to dealer
        dealer_hand = ['AS', 'KC']
        test_machine.shoe.pop(test_machine.shoe.index('AS'))
        test_machine.shoe.pop(test_machine.shoe.index('KC'))
        test_machine.dealer.current_hands.append(dealer_hand)
        # DEBUG - print dealer and player stats #
        test_machine.dealer.print_player_stats()
        first_player.print_player_stats()
        # Transition to INITIAL_SCORING and execute all methods within
        test_machine.transition(bjfsm.GameState.INITIAL_SCORING)
        test_machine.step()
        ## Test ##
        assert test_machine.state == bjfsm.GameState.BETTING
        assert first_player.White == 50
        assert first_player.Blue == 20
        assert len(test_machine.shoe) == 49


    def test_first_player_with_blackjack_regular_blackjack_is_handled_correctly_against_dealer_blackjack(self):
        pass


    def test_first_player_with_regular_hand_loses_correctly_against_dealer_blackjack(self):
        pass


    def test_first_player_with_two_regular_hands_loses_correctly_against_dealer_blackjack(self):
        pass


    def test_first_player_with_regular_hand_keeps_playing_after_checking_dealer_has_no_blackjack(self):
        pass


    def test_first_player_with_blackjack_wins_after_checking_dealer_has_no_blackjack(self):
        pass

    
    def test_first_player_with_regular_blackjack_hands_wins_just_second_after_checking_dealer_has_no_blackjack(self):
        pass


    def test_card_count_is_correct_for_single_deck_shoe_after_checking_for_dealer_blackjack_with_two_blackjacks(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # executes shuffle_cut_and_burn(None) in SHUFFLING
        # Manually deal player blackjack hand
        player_hand = ['QD', 'AH']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(player_hand)
        #print(first_player.current_hands[0])
        # Manually remove dealt player's blackjack hand cards from shoe
        if 'QD' in test_machine.discard:
            pass
        else:
            test_machine.shoe.remove('QD')
        if 'AH' in test_machine.discard:
            pass
        else:
            test_machine.shoe.remove('AH')
        # Manually deal blackjack hand to dealer
        dealer_hand = ['AS', 'KC']
        test_machine.dealer.current_hands.append(dealer_hand)
        print(test_machine.dealer.current_hands[0])
        # Remove manually dealt dealer's blackjack hand cards from shoe
        if 'AS' in test_machine.discard:
            pass
        else:
            test_machine.shoe.remove('AS')
        if 'KC' in test_machine.discard:
            pass
        else:
            test_machine.shoe.remove('KC')
        # Manually transition to SCORING
        test_machine.transition(bjfsm.GameState.SCORING)
        test_machine.step() # scores all players' hands, checks for and handles dealer and player blackjacks in SCORING
        # Verify card count between shoe and discard is correct for a single deck after checking for dealer blackjack
        assert (len(test_machine.shoe) + len(test_machine.discard)) == 54


    def test_card_count_is_correct_for_single_deck_shoe_after_SCORING(self):
        pass


class TestNoBlackjacks_INITIAL_SCORING:
    def test_blackjack_state_machine_transitions_to_INITIAL_SCORING_from_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        test_machine.step() # executes deal() in DEALING
        assert test_machine.state == bjfsm.GameState.INITIAL_SCORING



class TestTrackingNaturalBlackjacks:
    def test_first_player_with_one_blackjack_hand_has_it_tracked_correctly_in_INITIAL_SCORING(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        # Manually deal a blackjack hand to first player
        blackjack_hand = ['AH', 'QD']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(blackjack_hand)
        # Manually deal a random hand to dealer for score_all_hands_in_play() to work
        dealer_hand = ['8H', 'JC']
        test_machine.dealer.current_hands.append(dealer_hand)
        # Add each player and their respective blackjack hands to a dictionary inside score_all_hands_in_play()
        test_machine.score_all_hands_in_play()
        ## Test ##
        # Verify first player has only 1 blackjack hand
        first_player_tracked_blackjack_hands = test_machine.current_round_natural_blackjacks[first_player]
        assert len(first_player_tracked_blackjack_hands) == 1
        # Verify that tracked blackjack hand is the one that has been dealt
        first_player_tracked_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][0]
        assert first_player_tracked_blackjack_hand == blackjack_hand
    
    def test_first_player_with_two_blackjack_hands_has_them_tracked_correctly_in_INITIAL_SCORING(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        # Manually deal two blackjack hands to first player
        first_blackjack_hand = ['AH', 'QD']
        second_blackjack_hand = ['KC', 'AS']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(first_blackjack_hand)
        first_player.current_hands.append(second_blackjack_hand)
        # Manually deal a random hand to dealer for score_all_hands_in_play() to work
        dealer_hand = ['8H', 'JC']
        test_machine.dealer.current_hands.append(dealer_hand)
        # Add each player and their respective blackjack hands to a dictionary inside score_all_hands_in_play()
        test_machine.score_all_hands_in_play()
        ## Test ##
        # Verify first player has 2 blackjack hands
        first_player_tracked_blackjack_hands = test_machine.current_round_natural_blackjacks[first_player]
        assert len(first_player_tracked_blackjack_hands) == 2
        # Verify that tracked blackjack hands are the ones that have been dealt
        first_player_first_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][0]
        first_player_second_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][1]
        assert first_player_first_logged_blackjack_hand == first_blackjack_hand
        assert first_player_second_logged_blackjack_hand == second_blackjack_hand

    def test_first_player_with_blackjack_regular_blackjack_hands_has_blackjacks_tracked_correctly_in_INITIAL_SCORING(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        # Deal blackjack regular blackjack hands to first player
        first_hand = ['AH', 'QD']
        second_hand = ['8D', '4C']
        third_hand = ['KC', 'AS']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(first_hand)
        first_player.current_hands.append(second_hand)
        first_player.current_hands.append(third_hand)
        # Manually deal a random hand to dealer for score_all_hands_in_play() to work
        dealer_hand = ['8H', 'JC']
        test_machine.dealer.current_hands.append(dealer_hand)
        # Add each player and their respective blackjack hands to a dictionary within score method
        test_machine.score_all_hands_in_play()
        ## Test ##
        # Verify first player has 2 blackjack hands
        first_player_tracked_blackjack_hands = test_machine.current_round_natural_blackjacks[first_player]
        assert len(first_player_tracked_blackjack_hands) == 2
        # Verify dealt non-blackjack hand is not tracked
        assert second_hand not in first_player_tracked_blackjack_hands
        # Verify that tracked blackjack hands are the ones that have been dealt
        first_player_first_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][0]
        first_player_second_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][1]
        assert first_player_first_logged_blackjack_hand == first_hand
        assert first_player_second_logged_blackjack_hand == third_hand

    def test_one_player_one_natural_blackjack_none_tracked_after_INITIAL_SCORING(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        # Manually deal a blackjack hand to first player
        blackjack_hand = ['AH', 'QD']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(blackjack_hand)
        # Manually deal a random hand to dealer for score_all_hands_in_play() to work
        dealer_hand = ['8H', 'JC']
        test_machine.dealer.current_hands.append(dealer_hand)
        test_machine.transition(bjfsm.GameState.INITIAL_SCORING)
        test_machine.step() # executes all methods inside INITIAL_SCORING including score_all_hands_in_play()
        ## Test ##
        # Verify tracked blackjacks dictionary is empty after INITIAL_SCORING
        assert len(test_machine.current_round_natural_blackjacks) == 0

    def test_one_player_two_natural_blackjacks_none_tracked_after_INITIAL_SCORING(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        # Manually deal two blackjack hands to first player
        first_blackjack_hand = ['AH', 'QD']
        second_blackjack_hand = ['KC', 'AS']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(first_blackjack_hand)
        first_player.current_hands.append(second_blackjack_hand)
        # Manually deal a random hand to dealer for score_all_hands_in_play() to work
        dealer_hand = ['8H', 'JC']
        test_machine.dealer.current_hands.append(dealer_hand)
        test_machine.transition(bjfsm.GameState.INITIAL_SCORING)
        test_machine.step() # executes all methods inside INITIAL_SCORING including score_all_hands_in_play()
        ## Test ##
        # Verify tracked blackjacks dictionary is empty after INITIAL_SCORING
        assert len(test_machine.current_round_natural_blackjacks) == 0

    def test_one_player_blackjack_regular_blackjack_hands_none_tracked_after_INITIAL_SCORING(self):
        ## Setup ##
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # execute shuffle_cut_and_burn() in SHUFFLING
        # Deal blackjack regular blackjack hands to first player
        first_hand = ['AH', 'QD']
        second_hand = ['8D', '4C']
        third_hand = ['KC', 'AS']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(first_hand)
        first_player.current_hands.append(second_hand)
        first_player.current_hands.append(third_hand)
        # Manually deal a random hand to dealer for score_all_hands_in_play() to work
        dealer_hand = ['8H', 'JC']
        test_machine.dealer.current_hands.append(dealer_hand)
        test_machine.transition(bjfsm.GameState.INITIAL_SCORING)
        test_machine.step() # executes all methods inside INITIAL_SCORING including score_all_hands_in_play()
        ## Test ##
        # Verify tracked blackjacks dictionary is empty after INITIAL_SCORING
        assert len(test_machine.current_round_natural_blackjacks) == 0


class TestMiscellaneous:
    def test_invalid_state_transition_handled(self):
        BadState = Enum('BadState', ['InvalidState'])
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.transition(BadState.InvalidState)
        with pytest.raises(NameError):
            test_machine.step()

    """
    def test_player_hand_is_dealt_in_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.transition(bjfsm.GameState.DEALING)
        test_machine.step() # execute deal()
        assert len(test_machine.hand) == 2

    def test_starting_player_hand_is_scored_in_SCORING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.transition(bjfsm.GameState.DEALING)
        test_machine.step() # execute deal() and transition to SCORING
        test_machine.step() # execute score()
        assert (test_machine.score >= 4) and (test_machine.score <= 21)
    """


class TestReshuffling:
    def test_single_deck_shoe_not_reshuffled_at_or_before_min_pen_bound_of_fifty_percent(self, monkeypatch):
        # Shuffle single-deck shoe at 50% pen ('front_cut_card' is at index 26)
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING, assigning active player
        test_machine.shuffle_cut_and_burn(50)
        test_machine.transition(bjfsm.GameState.DEALING)
        # Step through the state machine enough times to deal 13 hands (26 cards)
        for x in range (0, 13):
            test_machine.step() # executes deal() in GameState.DEALING
            test_machine.step() # executes score_hand() in GameState.SCORING
            if test_machine.state == bjfsm.GameState.DEALING:
                pass
            elif test_machine.state == bjfsm.GameState.PLAYER_PLAYING:
                monkeypatch.setattr('builtins.input', lambda _: 'stand')
                test_machine.step() # executes play() in GameState.PLAYING /w supplied user input of 'stand'
        # Check that next card to be dealt is 'front_cut_card' and we haven't reshuffled yet
        assert test_machine.shoe[0] == 'front_cut_card'
        assert len(test_machine.shoe) == 27
        assert test_machine.state == bjfsm.GameState.DEALING
    
    def test_single_deck_shoe_is_reshuffled_only_after_min_pen_bound_of_fifty_percent(self, monkeypatch):
        # Shuffle single-deck shoe at 50% pen ('front_cut_card' is at index 26)
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.shuffle_cut_and_burn(50)
        test_machine.transition(bjfsm.GameState.DEALING)
        # Step through the state machine enough times to deal 14 hands (28 cards)
        for x in range (0, 14):
            test_machine.step() # executes deal() in GameState.DEALING
            test_machine.step() # executes score_hand() in GameState.SCORING
            if test_machine.state == bjfsm.GameState.DEALING:
                pass
            elif test_machine.state == bjfsm.GameState.PLAYING:
                monkeypatch.setattr('builtins.input', lambda _: 'stand')
                test_machine.step() # executes play() in GameState.PLAYING /w supplied user input of 'stand'
        # Verify state machine is reshuffling at round end after dealing 28 cards
        assert test_machine.state == bjfsm.GameState.SHUFFLING