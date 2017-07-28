"""Module to test genetic."""
from ai.AI import Neural
from ai import genetic
from django.test import TestCase


class GeneticTests(TestCase):
    """Testing for the genetic code."""

    def setUp(self):
        """Set a new game for testing."""
        self.game = genetic.Game()
        self.network = genetic.Network([18, 27, 9, 1])
        self.gen = genetic.Generation([])

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

    def test_get_move_gets_a_move(self):
        """Gets a move."""
        game = self.game
        move = self.network.get_move(game)
        self.assertTrue(move == 0)

    # ============ Iindividual tests =============== #

    def test_create_two_individuals(self):
        """Create two individuals."""
        test = self.gen
        test = test.new_random(2)
        test = test.new_random(2, [18, 27, 9, 1], 0, test.individuals)
        self.assertTrue(len(test.individuals) == 2)
        # import pdb; pdb.set_trace()

    def test_slice_two_individuals(self):
        """Create two individuals."""
        gen = self.gen
        gen = gen.new_random(2)
        indiv1 = gen.individuals[0]
        indiv2 = gen.individuals[1]
        splice = indiv1.splice(indiv1.net, indiv2.net)
        self.assertTrue(indiv1.net.layers is not indiv2.net.layers)
        self.assertTrue(splice.layers is not indiv1.net.layers)
        self.assertTrue(splice.layers is not indiv2.net.layers)
        flag = True
        for i in range(len(splice.layers) - 1):
            for j in range(len(splice.layers[i])):
                for k in range(len(splice.layers[i][j].weights)):
                    splice_weight = splice.layers[i][j].weights[k]
                    indiv_weight = indiv1.net.layers[i][j].weights[k]
                    if splice_weight is not indiv_weight:
                        flag = False
        self.assertFalse(flag)
        flag = True
        for i in range(len(splice.layers) - 1):
            for j in range(len(splice.layers[i])):
                for k in range(len(splice.layers[i][j].weights)):
                    splice_weight = splice.layers[i][j].weights[k]
                    indiv_weight = indiv2.net.layers[i][j].weights[k]
                    if splice_weight is not indiv_weight:
                        flag = False
        self.assertFalse(flag)

        def test_reproduce_new_individual(self):
            """Create new individual."""
            gen = self.gen
            gen = gen.new_random(2)
            indiv1 = gen.individuals[0]
            indiv2 = gen.individuals[1]
            repo = indiv1.reproduce(2, indiv2)
            self.assertTrue(indiv1.net.layers is not indiv2.net.layers)
            self.assertTrue(repo.layers is not indiv1.net.layers)
            flag = True
            for i in range(len(repo.layers) - 1):
                for j in range(len(repo.layers[i])):
                    for k in range(len(repo.layers[i][j].weights)):
                        repo_weight = repo.layers[i][j].weights[k]
                        indiv_weight = indiv1.net.layers[i][j].weights[k]
                        if repo_weight is not indiv_weight:
                            flag = False
            self.assertFalse(flag)

    # ============ Generation tests =============== #

    def test_run_runs(self):
        """Gen will run."""
        test = self.gen
        test = test.new_random(1)
        for i in range(1):
            test.run()
            test2 = test.next(.3, 1)
        self.assertNotEqual(test, test2)

    def test_export_import_match_original(self):
        """Test imported matches exported."""
        gen = self.gen
        gen = gen.new_random(5)
        exported = gen.export()
        imported = gen.gen_import(exported)
        for i in range(len(gen.individuals)):
            for j in range(len(gen.individuals[0].net.layers) - 1):
                for k in range(len(gen.individuals[0].net.layers[j])):
                    gen_node = gen.individuals[i].net.layers[j][k]
                    imported_node = imported.individuals[i].net.layers[j][k]
                    self.assertTrue(
                        gen_node.input == imported_node.input
                    )
                    self.assertTrue(
                        gen_node.threshold == imported_node.threshold
                    )
                    self.assertTrue(
                        gen_node.weights == imported_node.weights
                    )

