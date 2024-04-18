""" 
File: cut_helper_test.py
Author: Alexander Bulanov
"""

# Local Imports #
import lib.cut_helper as cut
import lib.blackjack_game_objects as bjo
import lib.blackjack_game_settings as bjs


class TestFirstCut:
    def test_single_deck_shoe_size_after_first_cut_becomes_53_cards(self):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        assert len(shoe) == 53

    def test_last_card_in_deck_after_first_cut_becomes_back_cut_card(self):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        assert shoe[-1] == 'back_cut_card'

    def test_first_fifteen_cards_become_last_fifteen_after_first_cut(self, monkeypatch):
        shoe = bjo.base_deck
        first_fifteen = shoe[0:15]
        #print(shoe)
        #print(first_fifteen)
        # Forcing first_cut_card_index to be 15
        monkeypatch.setattr('random.randrange', lambda first, last, step: 15)
        cut.first_cut(shoe)
        last_fifteen = shoe[-16:-1] # adjusted due to cut card moved to the end of a shoe
        #print(shoe)
        #print(last_fifteen)
        assert first_fifteen == last_fifteen

    def test_last_fifteen_cards_become_first_fifteen_after_first_cut(self, monkeypatch):
        shoe = bjo.base_deck
        last_fifteen = shoe[-15:]
        #print(shoe)
        #print(last_fifteen)
        # Forcing first_cut_card_index to be len(shoe)-15
        monkeypatch.setattr('random.randrange', lambda first, last, step: len(shoe)-15)
        cut.first_cut(shoe)
        first_fifteen = shoe[0:15]
        #print(shoe)
        #print(first_fifteen)
        assert last_fifteen == first_fifteen

    def test_single_deck_shoe_contains_one_of_each_card_after_first_cut(self):
        shoe = bjo.get_shoe_of_n_decks(1)
        cut.first_cut(shoe)
        # Verify deck contains correct number of copies of each non-cut card (1 of each for a single deck)
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        #print(shoe)
        for card in shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 1


class TestSecondCut:
    def test_single_deck_shoe_size_becomes_54_cards_after_second_cut(self):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        cut.second_cut(shoe, None)
        assert len(shoe) == 54

    def test_shoe_contains_front_cut_card_after_second_cut(self):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        cut.second_cut(shoe, None)
        assert 'front_cut_card' in shoe

    def test_single_deck_shoe_contains_one_of_each_card_after_second_cut(self):
        shoe = bjo.get_shoe_of_n_decks(1)
        cut.first_cut(shoe)
        cut.second_cut(shoe, None)
        # Verify deck contains correct number of copies of each non-cut card (1 of each for a single deck)
        card_occurrence_counts = dict.fromkeys(bjo.base_deck, 0)
        #print(shoe)
        for card in shoe:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                card_occurrence_counts[card] += 1
        for card in card_occurrence_counts:
            if (card != 'front_cut_card') and (card != 'back_cut_card'):
                print(card,"has",card_occurrence_counts[card],"occurrences in the shoe")
                assert card_occurrence_counts[card] == 1

    def test_front_cut_card_placed_at_min_pen_depth_for_single_deck_after_second_cut(self, monkeypatch):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        monkeypatch.setattr('random.randrange', lambda first, last, step: bjs.casino_deck_pen_percentage_bounds[1][0])
        cut.second_cut(shoe, None)
        assert 'front_cut_card' == shoe[27]

    def test_front_cut_card_placed_at_max_pen_depth_for_single_deck_after_second_cut(self, monkeypatch):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        monkeypatch.setattr('random.randrange', lambda first, last, step: bjs.casino_deck_pen_percentage_bounds[1][1])
        cut.second_cut(shoe, None)
        assert 'front_cut_card' == shoe[37]

    def test_front_cut_card_placed_in_valid_range_for_single_deck_after_second_cut(self):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        cut.second_cut(shoe, None)
        assert 'front_cut_card' in shoe[27:38]

    def test_back_cut_card_placed_at_end_of_shoe_after_second_cut(self):
        shoe = bjo.base_deck
        cut.first_cut(shoe)
        cut.second_cut(shoe, None)
        assert 'back_cut_card' == shoe[-1]