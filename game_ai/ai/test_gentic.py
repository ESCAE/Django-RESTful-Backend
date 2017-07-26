"""Module to test genetic."""
from ai.AI import Neural
from ai import genetic
from django.test import TestCase


class GeneticTests(TestCase):
    """Testing for the genetic code."""

    def setUp(self):
        """Set a new game for testing."""
        self.game = genetic.Game()
        self.network = genetic.Network(Neural([18, 27, 9, 1]))

    # =========== Game tests ========= #

    def test_properties_of_new_game(self):
        """Test a new games properties."""
        self.assertEqual(self.game.board, '         ')
        self.assertEqual(self.game.winner, None)
        self.assertEqual(self.game.history, [])
        self.assertEqual(self.game.turn, 'O')

    def test_empty_squares_empty_board(self):
        """Test the empty squares function with an empty board."""
        board = '         '
        self.assertEqual(
            list(range(len(board))), self.game.emptysquares(board)
        )

    def test_empty_squares_non_empty_board(self):
        """Test empty squares with some filled."""
        board = 'X  O XO  '
        self.assertEqual([1, 2, 4, 7, 8], self.game.emptysquares(board))

    def test_empty_squares_full_board(self):
        """Test empty squares of a full board."""
        board = 'XOOOXXXXO'
        self.assertEqual([], self.game.emptysquares(board))

    def test_move_updates_game(self):
        """Test move updates the game history."""
        self.assertEqual(self.game.history, [])
        board = '         '
        move = 5
        self.game.move(board, move)
        self.assertEqual(self.game.history, ['         '])
        self.assertEqual(self.game.board, '     O   ')
        self.assertEqual(self.game.turn, 'X')

    def test_undo_resets_game_to_previous(self):
        """Test that undo steps the history back and turn."""
        self.game.history = ['         ', '    X    ', '   OX    ']
        self.game.turn = 'X'
        self.game.undo()
        self.assertEqual(
            self.game.history, ['         ', '    X    ']
        )
        self.assertEqual(self.game.turn, 'O')

    # =========== Network tests =============== #

    def test_get_inputs_returns_expected_inputs(self):
        """Return inputs based on board and turn."""
        inputs = self.network.get_inputs('   OX    ', 'X')
        self.assertTrue(
            inputs == [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

    # def test_get_move_gets_a_move(self):
    #     """Gets a move."""
    #     game = self.game
    #     move = self.network.get_move(game)
    #     import pdb; pdb.set_trace()

    # ============ Iindividual tests =============== #

    # ============ Generation tests =============== #

    
