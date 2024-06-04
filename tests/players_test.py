""" 
File: players_test.py
Author: Alexander Bulanov
"""

# Global Imports #
import msvcrt
import pytest

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
        assert list(test_dealer.occupied_seats.keys()) == ['right_seat', 'center_seat', 'left_seat']
        for dealer_attr in tri_seat_player_attributes:
            assert getattr(test_dealer, dealer_attr)['right_seat'] == None
            assert getattr(test_dealer, dealer_attr)['left_seat'] == None
            if dealer_attr == 'occupied_seats':
                assert getattr(test_dealer, dealer_attr)['center_seat'] == 8 # casino dealer is always in 'center_seat' #8 at the table
            else:
                assert getattr(test_dealer, dealer_attr)['center_seat'] == None
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
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        # Test
        assert test_player.name == 'abulanov'
        assert test_player.is_dealer == False
        assert test_player.cash_balance == 100
        assert ((list(test_player.chips.keys()) == bjo.chip_names) and 
                (list(test_player.chips.values()) == expected_test_player_chip_pool))
        assert test_player.chip_pool_balance == 500
        assert test_player.hole_card_face_down == False
        assert list(test_player.occupied_seats.keys()) == ['right_seat', 'center_seat', 'left_seat']
        for player_attr in tri_seat_player_attributes:
            assert getattr(test_player, player_attr)['right_seat'] == None
            assert getattr(test_player, player_attr)['left_seat'] == None
            if player_attr == 'occupied_seats':
                assert getattr(test_player, player_attr)['center_seat'] == 1
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
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        # Test
        assert test_player.player_has_no_main_bets_in_play()
        assert test_player.player_has_no_side_bets_in_play()
        assert test_player.player_has_no_cards_in_play()


class TestPlayerBetting:
    def test_initial_bet_is_empty(self):
        # Setup
        tri_seat_player_bet_attributes = [
            'main_bets',
            'main_bet_amounts',
            'side_bets',
            'side_bet_amounts',
            ]
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        # Test
        for player_attr in tri_seat_player_bet_attributes:
            assert getattr(test_player, player_attr)['left_seat'] == None
            assert getattr(test_player, player_attr)['center_seat'] == None
            assert getattr(test_player, player_attr)['right_seat'] == None
        
    def test_single_seat_adding_one_Pink_chip_prints_error_message(self, monkeypatch, capfd):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100
        simulated_char_inputs = [b'2', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')

        captured = capfd.readouterr()
        expected_output = "Invalid (fractional) bet amount of $2.5 - please resubmit a bet /w an even number of Pink chips!\n"
        print(repr(captured.out))  # Print the captured output for debugging purposes
        assert captured.out == expected_output


    def test_single_seat_adding_one_of_each_White_Red_Blue_Green_chips_handled_correctly(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'1', b'3', b'4', b'5', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify 1 of each White/Red/Blue/Green chips are subtracted from test_player chip pool
        test_player_chip_pool_dict = test_player.chips
        for chip_color, chip_count in test_player_chip_pool_dict.items():
            if chip_color in ['Black', 'Purple', 'Yellow', 'Brown']:
                assert chip_count == 0
            else:
                pass
                if (chip_color == 'White'):
                    assert chip_count == 49
                elif (chip_color == 'Pink'):
                    assert chip_count == 30
                elif (chip_color == 'Red'):
                    assert chip_count == 19
                elif (chip_color == 'Blue'):
                    assert chip_count == 14
                elif (chip_color == 'Green'):
                    assert chip_count == 4
        # Verify 1 of each White/Red/Blue/Green chips are added to center_seat spot of test_player
        center_seat_bet_dict = test_player.main_bets['center_seat']
        for chip_color, chip_count in center_seat_bet_dict.items():
            if chip_color in ['White', 'Red', 'Blue', 'Green']:
                assert chip_count == 1
            else:
                assert chip_count == 0
        # Verify test_player chip_pool_balance has been reduced by $41
        assert test_player.chip_pool_balance == 500-41
        # Verify center_seat spot of test_player has main_bet value of $41
        assert test_player.main_bet_amounts['center_seat'] == 41

    def test_single_seat_adding_one_of_each_non_Pink_chip_only_adds_White_Red_Blue_Green_for_template_player(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'1', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify only 1 of each White/Red/Blue/Green chips are subtracted from test_player chip pool
        test_player_chip_pool_dict = test_player.chips
        for chip_color, chip_count in test_player_chip_pool_dict.items():
            if chip_color in ['Black', 'Purple', 'Yellow', 'Brown']:
                assert chip_count == 0
            else:
                pass
                if (chip_color == 'White'):
                    assert chip_count == 49
                elif (chip_color == 'Pink'):
                    assert chip_count == 30
                elif (chip_color == 'Red'):
                    assert chip_count == 19
                elif (chip_color == 'Blue'):
                    assert chip_count == 14
                elif (chip_color == 'Green'):
                    assert chip_count == 4
        # Verify only 1 of each White/Red/Blue/Green chips are added to center_seat spot of test_player
        center_seat_bet_dict = test_player.main_bets['center_seat']
        for chip_color, chip_count in center_seat_bet_dict.items():
            if chip_color in ['White', 'Red', 'Blue', 'Green']:
                assert chip_count == 1
            else:
                assert chip_count == 0
        # Verify test_player chip_pool_balance has been reduced by $41
        assert test_player.chip_pool_balance == 500-41
        # Verify center_seat spot of test_player has main_bet value of $41
        assert test_player.main_bet_amounts['center_seat'] == 41

    def test_single_seat_adding_one_of_each_chip_then_removing_all_but_one_White_handled_correctly(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9',
                                 b'(', b'*', b'&', b'^', b'%', b'$', b'#', b'@', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify only 1 White chip is subtracted from test_player chip pool
        test_player_chip_pool_dict = test_player.chips
        for chip_color, chip_count in test_player_chip_pool_dict.items():
            if chip_color in ['Black', 'Purple', 'Yellow', 'Brown']:
                assert chip_count == 0
            else:
                pass
                if (chip_color == 'White'):
                    assert chip_count == 49
                elif (chip_color == 'Pink'):
                    assert chip_count == 30
                elif (chip_color == 'Red'):
                    assert chip_count == 20
                elif (chip_color == 'Blue'):
                    assert chip_count == 15
                elif (chip_color == 'Green'):
                    assert chip_count == 5
        # Verify only 1 White chip is added to center_seat spot of test_player
        center_seat_bet_dict = test_player.main_bets['center_seat']
        for chip_color, chip_count in center_seat_bet_dict.items():
            if chip_color == 'White':
                assert chip_count == 1
            else:
                assert chip_count == 0
        # Verify test_player chip_pool_balance has been reduced by $1
        assert test_player.chip_pool_balance == 500-1
        # Verify center_seat spot of test_player has main_bet value of $1
        assert test_player.main_bet_amounts['center_seat'] == 1
        
    def test_single_seat_adding_one_of_each_chip_then_resetting_bet_and_adding_two_Green_handled_correctly(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'r', b'5', b'5', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify only 2 Green chips subtracted from test_player chip pool
        test_player_chip_pool_dict = test_player.chips
        for chip_color, chip_count in test_player_chip_pool_dict.items():
            if chip_color in ['Black', 'Purple', 'Yellow', 'Brown']:
                assert chip_count == 0
            else:
                pass
                if (chip_color == 'White'):
                    assert chip_count == 50
                elif (chip_color == 'Pink'):
                    assert chip_count == 30
                elif (chip_color == 'Red'):
                    assert chip_count == 20
                elif (chip_color == 'Blue'):
                    assert chip_count == 15
                elif (chip_color == 'Green'):
                    assert chip_count == 3
        # Verify only 2 Green chips are added to center_seat spot of test_player
        center_seat_bet_dict = test_player.main_bets['center_seat']
        for chip_color, chip_count in center_seat_bet_dict.items():
            if chip_color == 'Green':
                assert chip_count == 2
            else:
                assert chip_count == 0
        # Verify test_player chip_pool_balance has been reduced by $50
        assert test_player.chip_pool_balance == 500-50
        # Verify center_seat spot of test_player has main_bet value of $50
        assert test_player.main_bet_amounts['center_seat'] == 50

    def test_single_seat_betting_one_Red_two_Pink_chips_has_correct_chip_pool_balance_and_bet_amounts_as_ints(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'3', b'2', b'2', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify test_player chip_pool_balance is reduced by $10 and is an int() datatype
        assert test_player.chip_pool_balance == 500-10
        assert type(test_player.chip_pool_balance) == int
        # Verify center_seat spot of test_player has main_bet value of $10 and is an int() datatype
        assert test_player.main_bet_amounts['center_seat'] == 10
        assert type(test_player.main_bet_amounts['center_seat']) == int

    def test_single_seat_betting_one_Blue_Green_Pink_remove_Pink_has_correct_chip_pool_balance_and_bet_amounts_as_ints(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'4', b'5', b'2', b'@', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify test_player chip_pool_balance is reduced by $35 and is an int() datatype
        assert test_player.chip_pool_balance == 500-35
        assert type(test_player.chip_pool_balance) == int
        # Verify center_seat spot of test_player has main_bet value of $35 and is an int() datatype
        assert test_player.main_bet_amounts['center_seat'] == 35
        assert type(test_player.main_bet_amounts['center_seat']) == int

    def test_single_seat_betting_one_Blue_Green_Pink_reset_then_betting_one_Green_has_correct_chip_pool_balance_and_bet_amounts_as_ints(self, monkeypatch):
        # Setup
        test_username = 'abulanov'
        test_seat = 1
        test_player = bjp.Player.create_new_player_from_template(test_username, test_seat)
        table_min = 1
        table_max = 100      
        simulated_char_inputs = [b'4', b'5', b'2', b'r', b'5', b'f']
        iterable_simulated_char_inputs = iter(simulated_char_inputs)
        test_player.init_main_seat_bet_fields('center_seat')
        for i in range(0, len(simulated_char_inputs)):
            monkeypatch.setattr('msvcrt.getch', lambda: next(iterable_simulated_char_inputs))
            test_player.get_bet_input_character(table_min, table_max, 'center_seat')
        #test_player.print_player_stats()
        # Verify test_player chip_pool_balance is reduced by $25 and is an int() datatype
        assert test_player.chip_pool_balance == 500-25
        assert type(test_player.chip_pool_balance) == int
        # Verify center_seat spot of test_player has main_bet value of $25 and is an int() datatype
        assert test_player.main_bet_amounts['center_seat'] == 25
        assert type(test_player.main_bet_amounts['center_seat']) == int

