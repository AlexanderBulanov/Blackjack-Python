""" 
File: players_test.py
Author: Alexander Bulanov
"""

# Local Imports #
import lib.blackjack_players as bjp


class TestBetMaking:
    def test_template_player_hand_bet_set_correctly(self):
        player = bjp.Player.create_new_player_from_template('Alex')
        # Bet is placed on a spot at the table, without knowing what the hand will be
        bet = '2 White, 1 Blue'
        player.add_primary_bet(hand, bet)
        hand = ['AH', 'QD']
        """
        DEBUG:
        """
        player.print_player_stats()
        assert 2 == 3