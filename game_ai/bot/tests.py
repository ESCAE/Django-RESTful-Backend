"""."""
from django.test import TestCase
from bot import tic_tack


# Create your tests here.
class TicTacTest(TestCase):
    """."""

    def test_check_move_true(self):
        self.assertEqual(tic_tack.check_move([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 0), True)

    def test_check_move_False(self):
        self.assertEqual(tic_tack.check_move(['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 0), False)

    def test_winner_None(self):
        self.assertEqual(tic_tack.winner([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 'X')[0], None)

    def test_winner_True_X_012(self):
        self.assertEqual(tic_tack.winner(['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' '], 'X')[0], True)

    def test_winner_False_O_012(self):
        self.assertEqual(tic_tack.winner(['O', 'O', 'O', ' ', ' ', ' ', ' ', ' ', ' '], 'O')[0], False)

    def test_winner_True_X_036(self):
        self.assertEqual(tic_tack.winner(['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' '], 'X')[0], True)

    def test_winner_False_O_036(self):
        self.assertEqual(tic_tack.winner(['O', ' ', ' ', 'O', ' ', ' ', 'O', ' ', ' '], 'O')[0], False)

    def test_winner_True_X_048(self):
        self.assertEqual(tic_tack.winner(['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X'], 'X')[0], True)

    def test_winner_False_O_048(self):
        self.assertEqual(tic_tack.winner(['O', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'O'], 'O')[0], False)

    def test_winner_True_X_147(self):
        self.assertEqual(tic_tack.winner([' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X', ' '], 'X')[0], True)

    def test_winner_False_O_147(self):
        self.assertEqual(tic_tack.winner([' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O', ' '], 'O')[0], False)

    def test_winner_True_X_258(self):
        self.assertEqual(tic_tack.winner([' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', 'X'], 'X')[0], True)

    def test_winner_False_O_258(self):
        self.assertEqual(tic_tack.winner([' ', ' ', 'O', ' ', ' ', 'O', ' ', ' ', 'O'], 'O')[0], False)

    def test_winner_True_X_246(self):
        self.assertEqual(tic_tack.winner([' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' '], 'X')[0], True)

    def test_winner_False_O_246(self):
        self.assertEqual(tic_tack.winner([' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' '], 'O')[0], False)

    def test_winner_True_X_345(self):
        self.assertEqual(tic_tack.winner([' ', ' ', ' ', 'X', 'X', 'X', ' ', ' ', ' '], 'X')[0], True)

    def test_winner_False_O_345(self):
        self.assertEqual(tic_tack.winner([' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' '], 'O')[0], False)

    def test_winner_True_X_678(self):
        self.assertEqual(tic_tack.winner([' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X'], 'X')[0], True)

    def test_winner_False_O_678(self):
        self.assertEqual(tic_tack.winner([' ', ' ', ' ', ' ', ' ', ' ', 'O', 'O', 'O'], 'O')[0], False)

    def test_new_board(self):
        self.assertEqual(type(tic_tack.new_board('         ', 2)), dict)

    def test_directory(self):
        self.assertEqual(type(tic_tack.directory('         ', 2)), dict)

    def test_new_board_bot(self):
        self.assertEqual(type(tic_tack.new_board_bot([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 2)), list)

    def test_greedy_bot(self):
        self.assertEqual(type(tic_tack.greedy_bot([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])), int)

    def test_dumb_bot(self):
        self.assertEqual(type(tic_tack.dumb_bot([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])), int)
