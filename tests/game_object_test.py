""" 
File: game_object_test.py
Author: Alexander Bulanov
"""

# Local Imports #
import lib.blackjack_game_objects as bjo

class TestDeckBuilder:
    def test_single_deck_built_shoe_is_equivalent_to_base_deck(self):
        # Build shoe out of 1 deck of cards
        built_shoe = bjo.get_shoe_of_n_decks(1)
        assert set(built_shoe) == set(bjo.base_deck)
    
    def test_one_deck_shoe_built_correctly(self):
        # Build shoe out of 1 deck of cards
        built_shoe = bjo.get_shoe_of_n_decks(1)
        # Create a dictionary to track occurrences of each card in built shoe
        card_occurrences = dict.fromkeys(bjo.base_deck, 0)
        # Tally up number of times each card is encountered
        for shoe_card in built_shoe:
            if shoe_card in card_occurrences.keys():
                card_occurrences[shoe_card] += 1
        """
        for card in card_occurrences.keys():
            print(card,"has",card_occurrences[card],"occurrences")
        """
        # Check that shoe contains 52 cards
        assert len(built_shoe) == 52
        # Check each card is encountered only once for a single deck shoe
        for card in card_occurrences.keys():
            assert card_occurrences[card] == 1

    def test_two_deck_shoe_built_correctly(self):
        # Build shoe out of 1 deck of cards
        built_shoe = bjo.get_shoe_of_n_decks(2)
        # Create a dictionary to track occurrences of each card in built shoe
        card_occurrences = dict.fromkeys(bjo.base_deck, 0)
        # Tally up number of times each card is encountered
        for shoe_card in built_shoe:
            if shoe_card in card_occurrences.keys():
                card_occurrences[shoe_card] += 1
        """
        for card in card_occurrences.keys():
            print(card,"has",card_occurrences[card],"occurrences")
        """
        # Check that shoe contains 52*2 cards
        assert len(built_shoe) == 52*2
        # Check each card is encountered only once for a single deck shoe
        for card in card_occurrences.keys():
            assert card_occurrences[card] == 2

    def test_four_deck_shoe_built_correctly(self):
        # Build shoe out of 1 deck of cards
        built_shoe = bjo.get_shoe_of_n_decks(4)
        # Create a dictionary to track occurrences of each card in built shoe
        card_occurrences = dict.fromkeys(bjo.base_deck, 0)
        # Tally up number of times each card is encountered
        for shoe_card in built_shoe:
            if shoe_card in card_occurrences.keys():
                card_occurrences[shoe_card] += 1
        """
        for card in card_occurrences.keys():
            print(card,"has",card_occurrences[card],"occurrences")
        """
        # Check that shoe contains 52*4 cards
        assert len(built_shoe) == 52*4
        # Check each card is encountered only once for a single deck shoe
        for card in card_occurrences.keys():
            assert card_occurrences[card] == 4

    def test_six_deck_shoe_built_correctly(self):
        # Build shoe out of 1 deck of cards
        built_shoe = bjo.get_shoe_of_n_decks(6)
        # Create a dictionary to track occurrences of each card in built shoe
        card_occurrences = dict.fromkeys(bjo.base_deck, 0)
        # Tally up number of times each card is encountered
        for shoe_card in built_shoe:
            if shoe_card in card_occurrences.keys():
                card_occurrences[shoe_card] += 1
        """
        for card in card_occurrences.keys():
            print(card,"has",card_occurrences[card],"occurrences")
        """
        # Check that shoe contains 52*6 cards
        assert len(built_shoe) == 52*6
        # Check each card is encountered only once for a single deck shoe
        for card in card_occurrences.keys():
            assert card_occurrences[card] == 6

    def test_eight_deck_shoe_built_correctly(self):
        # Build shoe out of 1 deck of cards
        built_shoe = bjo.get_shoe_of_n_decks(8)
        # Create a dictionary to track occurrences of each card in built shoe
        card_occurrences = dict.fromkeys(bjo.base_deck, 0)
        # Tally up number of times each card is encountered
        for shoe_card in built_shoe:
            if shoe_card in card_occurrences.keys():
                card_occurrences[shoe_card] += 1
        """
        for card in card_occurrences.keys():
            print(card,"has",card_occurrences[card],"occurrences")
        """
        # Check that shoe contains 52*8 cards
        assert len(built_shoe) == 52*8
        # Check each card is encountered only once for a single deck shoe
        for card in card_occurrences.keys():
            assert card_occurrences[card] == 8