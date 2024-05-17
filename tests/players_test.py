""" 
File: players_test.py
Author: Alexander Bulanov
"""

# Local Imports #
import lib.blackjack_players as bjp
import lib.blackjack_game_objects as bjo

class TestPlayerCreation:
    def test_casino_dealer_created_correctly_from_template(self):
        # Setup
        tri_seat_player_attributes = [
            'occupied_seats',
            'main_bets',
            'main_bet_amounts',
            'side_bets',
            'side_bet_amounts',
            'hands',
            'hand_scores'
            ]
        test_dealer = bjp.Player.create_casino_dealer()
        # Test
        assert test_dealer.name == 'Dealer'
        assert test_dealer.is_dealer == True
        assert test_dealer.cash_balance == 10000
        assert (list(test_dealer.chips.keys()) == bjo.chip_names) and (list(test_dealer.chips.values()) == 9*[1000])
        assert test_dealer.chip_pool_balance == 6643500
        assert test_dealer.hole_card_face_down == True
        assert list(test_dealer.occupied_seats.keys()) == ['left_seat', 'center_seat', 'right_seat']
        for dealer_attr in tri_seat_player_attributes:
            assert getattr(test_dealer, dealer_attr)['left_seat'] == None
            assert getattr(test_dealer, dealer_attr)['center_seat'] == None
            assert getattr(test_dealer, dealer_attr)['right_seat'] == None
        assert test_dealer.action == None

    def test_new_player_created_correctly_from_template(self):
        # Setup
        tri_seat_player_attributes = [
            'occupied_seats',
            'main_bets',
            'main_bet_amounts',
            'side_bets',
            'side_bet_amounts',
            'hands',
            'hand_scores'
            ]
        expected_test_player_chip_pool = [50, 30, 20, 15, 5, 0, 0, 0, 0]
        test_username = 'username'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        # Test
        assert test_player.name == test_username
        assert test_player.is_dealer == False
        assert test_player.cash_balance == 100
        assert ((list(test_player.chips.keys()) == bjo.chip_names) and 
                (list(test_player.chips.values()) == expected_test_player_chip_pool))
        assert test_player.chip_pool_balance == 500
        assert test_player.hole_card_face_down == False
        assert list(test_player.occupied_seats.keys()) == ['left_seat', 'center_seat', 'right_seat']
        for player_attr in tri_seat_player_attributes:
            assert getattr(test_player, player_attr)['left_seat'] == None
            assert getattr(test_player, player_attr)['right_seat'] == None
            if player_attr == 'occupied_seats':
                assert getattr(test_player, player_attr)['center_seat'] == test_seat
            else:
                assert getattr(test_player, player_attr)['center_seat'] == None
        assert test_player.action == None

    def test_dealer_created_from_template_has_no_bets_or_cards_in_play(self):
        # Setup
        test_dealer = bjp.Player.create_casino_dealer()
        # Test
        assert test_dealer.player_has_no_main_bets_in_play()
        assert test_dealer.player_has_no_side_bets_in_play()
        assert test_dealer.player_has_no_cards_in_play()

    def test_new_player_created_from_template_has_no_bets_or_cards_in_play(self):
        # Setup
        test_username = 'username'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        # Test
        assert test_player.player_has_no_main_bets_in_play()
        assert test_player.player_has_no_side_bets_in_play()
        assert test_player.player_has_no_cards_in_play()





"""
class TestBetMaking:
    def test_template_player_hand_bet_set_correctly(self, monkeypatch):
        player = bjp.Player.create_new_player_from_template('Alex')
        # Bet is placed on a spot at the table, without knowing what the hand will be
        bet = '2 White, 1 Blue'
        player.add_primary_bet(hand, bet)
        hand = ['AH', 'QD']
        player.print_player_stats()
        assert 2 == 3
"""