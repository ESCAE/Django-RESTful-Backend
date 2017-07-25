from django.test import TestCase
from ai.AI import Neural, Node


class AITestCase(TestCase):
    def setUp(self):
        self.networks = [Neural([2, 3, 2]), Neural([2, 3, 4, 2]), Neural([[2, 3, 2], [2, 3, 2], [2, 3, 2]])]


    def test_network_creates_node_objects(self):
        for network in self.networks:
            for layer in network.nodes:
                for node in layer:
                    self.assertIsInstance(node, Node)


    def test_network_sizes_return_correctly(self):
        self.assertEqual(self.networks[0].get_sizes(self.networks[0].nodes), [2, 3, 2])
        self.assertEqual(self.networks[1].get_sizes(self.networks[1].nodes), [2, 3, 4, 2])
        self.assertEqual(self.networks[2].get_sizes(self.networks[2].nodes), [3, 3, 3])

    def test_network_returns_proper_weights(self):
        self.assertEqual(self.networks[0]._get_weights(), [[[0, 0, 0], [0, 0, 0]], [[0, 0], [0, 0], [0, 0]], [[], []]])
        self.assertEqual(self.networks[1]._get_weights(), [[[0, 0, 0], [0, 0, 0]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[], []]])
        self.assertEqual(self.networks[2]._get_weights(), [[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[], [], []]])
    def test_network_reassigns_weights_properly(self):
        weight1 = [[[1, 1, 1], [1, 1, 1]], [[1, 1], [1, 1], [1, 1]], [[], []]]
        weight2 = [[[0, 1, 2], [3, 4, 5]], [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], [[0, 0], [0, 0], [0, 0], [0, 0]], [[], []]]
        weight3 = [[[17, 17, 17], [17, 17, 17], [17, 17, 17]], [[17, 17, 17], [17, 17, 17], [17, 17, 17]], [[], [], []]]
        self.networks[0]._set_weights(weight1)
        self.networks[1]._set_weights(weight2)
        self.networks[2]._set_weights(weight3)
        self.assertEqual(self.networks[0]._get_weights(), weight1)
        self.assertEqual(self.networks[1]._get_weights(), weight2)
        self.assertEqual(self.networks[2]._get_weights(), weight3)
    def test_run_raises_index_error_with_improper_input(self):
        self.assertRaises(IndexError, self.networks[0].run, [1])
        self.assertRaises(IndexError, self.networks[1].run, [1])
        self.assertRaises(IndexError, self.networks[2].run, [1,1])
    # def test_run_provides_proper_output(self):
    #     weight1 = [[[1, 1, 1], [1, 1, 1]], [[1, 1], [1, 1], [1, 1]], [[], []]]
    #     weight2 = [[[1, 1, 1], [1, 1, 1]], [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], [[1, 1], [1, 1], [1, 1], [1, 1]], [[], []]]
    #     weight3 = [[[0, 0, 0], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[], [], []]]
    #     self.networks[0]._set_weights(weight1)
    #     self.networks[1]._set_weights(weight2)
    #     self.networks[2]._set_weights(weight3)
    #     print('----------+++++++++++')
    #     print(self.networks[0].run([1, 0]))
    #     self.assertEqual(self.networks[0].run([1, 1]), [6, 6])
    #     self.assertEqual(self.networks[0].run([1, 0]), [3, 3])
    #     self.assertEqual(self.networks[1].run([1, 1]), [24, 24])
    #     self.assertEqual(self.networks[1].run([1, 0]), [12, 12])
    #     self.assertEqual(self.networks[2].run([1, 1]), [0, 0])
    #     self.assertEqual(self.networks[2].run([1, 0]), [0, 0])