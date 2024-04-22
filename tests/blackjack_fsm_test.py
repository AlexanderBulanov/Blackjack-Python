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
import lib.blackjack_game_logic as bjl
import lib.cut_helper as cuthlpr


class TestMachine:
    def test_beginning_state_is_STARTING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        assert test_machine.state == bjfsm.GameState.STARTING

    def test_invalid_state_transition_handled(self):
        BadState = Enum('BadState', ['InvalidState'])
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.transition(BadState.InvalidState)
        with pytest.raises(NameError):
            test_machine.step()

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


class TestShoeSetup:
    def test_single_deck_shoe_set_up_correctly_at_min_hardcoded_pen_bound_of_fifty_percent(self):
        ### Setup ###
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at minimum pen (50%) for a single deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][0])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and minimum (50%) pen percentage for a single deck shoe
        assert len(test_machine.shoe) == 1+52*1
        assert test_machine.pen == 50
        # Verify cut cards are present and are placed correctly at minimum (50%) pen for a single deck shoe
        assert test_machine.shoe[26] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 1 copy of each non-cut card across shoe and discard, for a single deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 1

    def test_single_deck_shoe_set_up_correctly_at_max_hardcoded_pen_bound_of_seventy_percent(self):
        ### Setup ###
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at maximum pen (70%) for a single deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][1])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and maximum (70%) pen percentage for a single deck shoe
        assert len(test_machine.shoe) == 1+52*1
        assert test_machine.pen == 70
        # Verify cut cards are present and are placed correctly at maximum (70%) pen for a single deck shoe
        assert test_machine.shoe[36] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 1 copy of each non-cut card across shoe and discard, for a single deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 1

    def test_double_deck_shoe_set_up_correctly_at_min_hardcoded_pen_bound_of_fifty_five_percent(self):
        ### Setup ###
        num_of_decks = 2
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at minimum pen (55%) for a double deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][0])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and minimum (55%) pen percentage for a double deck shoe
        assert len(test_machine.shoe) == 1+52*2
        assert test_machine.pen == 55
        # Verify cut cards are present and are placed correctly at minimum (55%) pen for a double deck shoe
        assert test_machine.shoe[57] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 2 copies of each non-cut card across shoe and discard, for a double deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 2

    def test_double_deck_shoe_set_up_correctly_at_max_hardcoded_pen_bound_of_seventy_five_percent(self):
        ### Setup ###
        num_of_decks = 2
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at maximum pen (75%) for a double deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][1])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and maximum (75%) pen percentage for a double deck shoe
        assert len(test_machine.shoe) == 1+52*2
        assert test_machine.pen == 75
        # Verify cut cards are present and are placed correctly at maximum (75%) pen for a double deck shoe
        assert test_machine.shoe[78] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 2 copies of each non-cut card across shoe and discard, for a double deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 2

    def test_four_deck_shoe_set_up_correctly_at_min_hardcoded_pen_bound_of_sixty_percent(self):
        ### Setup ###
        num_of_decks = 4
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at minimum pen (60%) for a four-deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][0])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and minimum (60%) pen percentage for a four-deck shoe
        assert len(test_machine.shoe) == 1+52*4
        assert test_machine.pen == 60
        # Verify cut cards are present and are placed correctly at minimum (60%) pen for a four-deck shoe
        assert test_machine.shoe[124] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 4 copies of each non-cut card across shoe and discard, for a four-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 4

    def test_four_deck_shoe_set_up_correctly_at_max_hardcoded_pen_bound_of_eighty_percent(self):
        ### Setup ###
        num_of_decks = 4
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at maximum pen (80%) for a four-deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][1])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and maximum (80%) pen percentage for a four-deck shoe
        assert len(test_machine.shoe) == 1+52*4
        assert test_machine.pen == 80
        # Verify cut cards are present and are placed correctly at maximum (80%) pen for a four-deck
        assert test_machine.shoe[166] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 4 copies of each non-cut card across shoe and discard, for a four-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 4

    def test_six_deck_shoe_set_up_correctly_at_min_hardcoded_pen_bound_of_sixty_five_percent(self):
        ### Setup ###
        num_of_decks = 6
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at minimum pen (65%) for a six-deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][0])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and minimum (65%) pen percentage for a six-deck shoe
        assert len(test_machine.shoe) == 1+52*6
        assert test_machine.pen == 65
        # Verify cut cards are present and are placed correctly at minimum (65%) pen for a six-deck shoe
        assert test_machine.shoe[202] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 6 copies of each non-cut card across shoe and discard, for a six-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 6

    def test_six_deck_shoe_set_up_correctly_at_max_hardcoded_pen_bound_of_eighty_five_percent(self):
        ### Setup ###
        num_of_decks = 6
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at maximum pen (85%) for a six-deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][1])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and maximum (85%) pen percentage for a six-deck shoe
        assert len(test_machine.shoe) == 1+52*6
        assert test_machine.pen == 85
        # Verify cut cards are present and are placed correctly at maximum (85%) pen for a six-deck shoe
        assert test_machine.shoe[265] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 6 copies of each non-cut card across shoe and discard, for a six-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 6

    def test_eight_deck_shoe_set_up_correctly_at_min_hardcoded_pen_bound_of_seventy_percent(self):
        ### Setup ###
        num_of_decks = 8
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at minimum pen (70%) for an eight-deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][0])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and minimum (70%) pen percentage for an eight-deck shoe
        assert len(test_machine.shoe) == 1+52*8
        assert test_machine.pen == 70
        # Verify cut cards are present and are placed correctly at minimum (70%) pen for an eight-deck shoe
        assert test_machine.shoe[291] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 8 copies of each non-cut card across shoe and discard, for an eight-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 8

    def test_eight_deck_shoe_set_up_correctly_at_max_hardcoded_pen_bound_of_ninety_percent(self):
        ### Setup ###
        num_of_decks = 8
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # First Cut
        cuthlpr.first_cut(test_machine.shoe)
        # Second Cut at maximum pen (90%) for an eight-deck shoe
        test_machine.pen = cuthlpr.second_cut(
            test_machine.shoe, bjs.casino_deck_pen_percentage_bounds[num_of_decks][1])
        # Burn the first card in shoe
        test_machine.discard.extend([test_machine.shoe.pop(0)])

        ### Checking Shoe Integrity ###
        # Verify deck size and maximum (90%) pen percentage for an eight-deck shoe
        assert len(test_machine.shoe) == 1+52*8
        assert test_machine.pen == 90
        # Verify cut cards are present and are placed correctly at maximum (90%) pen for an eight-deck shoe
        assert test_machine.shoe[374] == 'front_cut_card'
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 8 copies of each non-cut card across shoe and discard, for an eight-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 8


class TestShuffling:
    def test_starting_single_deck_shoe_is_shuffle_cut_and_burned_correctly_in_SHUFFLING(self):
        ### Setup ###
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.transition(bjfsm.GameState.SHUFFLING)
        test_machine.step() # execute shuffle_cut_and_burn()

        ### Checking Shoe Integrity ###
        # Verify deck size and pen percentage is in-bounds for a single deck shoe
        assert len(test_machine.shoe) == 1+52*1
        assert test_machine.pen in range(50, 70)
        # Verify cut cards are present and are placed correctly in-bounds for a single deck shoe
        assert 'front_cut_card' in test_machine.shoe[26:37]
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 1 copy of each non-cut card across shoe and discard, for a single deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 1

    def test_starting_eight_deck_shoe_is_shuffle_cut_and_burned_correctly_in_SHUFFLING(self):
        ### Setup ###
        num_of_decks = 8
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.transition(bjfsm.GameState.SHUFFLING)
        test_machine.step() # executes shuffle_cut_and_burn()
        ### Checking Shoe Integrity ###
        # Verify deck size and pen percentage is in-bounds for an eight-deck shoe
        assert len(test_machine.shoe) == 1+52*8
        assert test_machine.pen in range(70, 90)
        # Verify cut cards are present and are placed correctly in-bounds for an eight-deck shoe
        assert 'front_cut_card' in test_machine.shoe[291:375]
        assert test_machine.shoe[-1] == 'back_cut_card'
        # Verify there's 8 copies of each non-cut card across shoe and discard, for an eight-deck shoe
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        for card in test_machine.shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        if (len(test_machine.discard) == 1):
            card_occurrence_counts[test_machine.discard[0]] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                #print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 8

    def test_single_deck_shoe_not_reshuffled_at_or_before_min_pen_bound_of_fifty_percent(self, monkeypatch):
        # Shuffle single-deck shoe at 50% pen ('front_cut_card' is at index 26)
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
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


class TestPlayerSetup:
    def test_first_player_set_to_active_in_STARTING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        assert test_machine.active_player == test_machine.joined_players[0]

    def test_first_player_has_one_hand_dealt_in_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # executes shuffle_cut_and_burn(None) in SHUFFLING
        test_machine.step() # executes deal() in DEALING
        assert len(test_machine.joined_players[0].current_hands) == 1

    def test_dealer_has_one_hand_dealt_in_DEALING(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        test_machine.step() # executes start_game() in STARTING
        test_machine.step() # executes shuffle_cut_and_burn(None) in SHUFFLING
        test_machine.step() # executes deal() in DEALING
        assert len(test_machine.dealer.current_hands) == 1

    def test_first_player_with_one_blackjack_hand_has_it_tracked_correctly(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Deal a blackjack hand to first player
        blackjack_hand = ['AH', 'QD']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(blackjack_hand)
        # Add each player and their respective blackjack hands to a dictionary within score method
        test_machine.score_all_joined_players_hands()
        first_player_tracked_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][0]
        assert first_player_tracked_blackjack_hand == blackjack_hand

    def test_first_player_with_two_blackjack_hands_has_them_tracked_correctly(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Deal a blackjack hand to first player
        first_blackjack_hand = ['AH', 'QD']
        second_blackjack_hand = ['KC', 'AS']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(first_blackjack_hand)
        first_player.current_hands.append(second_blackjack_hand)
        # Add each player and their respective blackjack hands to a dictionary within score method
        test_machine.score_all_joined_players_hands()
        #print(first_player.current_hands)
        #print(test_machine.current_round_natural_blackjacks)
        first_player_first_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][0]
        first_player_second_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][1]
        assert first_player_first_logged_blackjack_hand == first_blackjack_hand
        assert first_player_second_logged_blackjack_hand == second_blackjack_hand

    def test_first_player_with_blackjack_regular_blackjack_hands_has_blackjacks_tracked_correctly(self):
        num_of_decks = 1
        test_machine = bjfsm.BlackjackStateMachine(num_of_decks)
        # Deal a blackjack hand to first player
        first_hand = ['AH', 'QD']
        second_hand = ['8D', '4C']
        third_hand = ['KC', 'AS']
        first_player = test_machine.joined_players[0]
        first_player.current_hands.append(first_hand)
        first_player.current_hands.append(second_hand)
        first_player.current_hands.append(third_hand)
        # Add each player and their respective blackjack hands to a dictionary within score method
        test_machine.score_all_joined_players_hands()
        #print(first_player.current_hands)
        #print(test_machine.current_round_natural_blackjacks)
        first_player_first_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][0]
        first_player_second_logged_blackjack_hand = test_machine.current_round_natural_blackjacks[first_player][1]
        assert first_player_first_logged_blackjack_hand == first_hand
        assert first_player_second_logged_blackjack_hand == third_hand
        