"""Module tests Neuro Network."""
from ai.AI import Neural
from ai.AI import Node
from django.test import TestCase


class AITestCase(TestCase):
    """Test Nuero Network."""

    def setUp(self):
        """Test setup."""
        self.networks = [
            Neural([2, 3, 2]), Neural([2, 3, 4, 2]),
            Neural([[2, 3, 2], [2, 3, 2], [2, 3, 2]])
        ]

    def test_network_creates_node_objects(self):
        """Test network creates a node objects."""
        for network in self.networks:
            for layer in network.layers:
                for node in layer:
                    self.assertIsInstance(node, Node)

    def test_network_sizes_return_correctly(self):
        """Test size is correct."""
        self.assertEqual(
            self.networks[0].get_sizes(self.networks[0].layers),
            [2, 3, 2]
        )
        self.assertEqual(
            self.networks[1].get_sizes(self.networks[1].layers),
            [2, 3, 4, 2]
        )
        self.assertEqual(
            self.networks[2].get_sizes(self.networks[2].layers),
            [3, 3, 3]
        )

    def test_network_returns_proper_weights(self):
        """Test network returns proper weights."""
        self.assertEqual(
            self.networks[0]._get_weights(),
            [[[0, 0, 0], [0, 0, 0]], [[0, 0], [0, 0], [0, 0]], [[], []]]
        )
        self.assertEqual(
            self.networks[1]._get_weights(),
            [
                [[0, 0, 0], [0, 0, 0]],
                [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                [[0, 0], [0, 0], [0, 0], [0, 0]],
                [[], []]
            ]
        )
        self.assertEqual(
            self.networks[2]._get_weights(),
            [
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                [[], [], []]
            ]
        )

    def test_network_reassigns_weights_properly(self):
        """Test weights get adjusted."""
        weight1 = [
            [[1, 1, 1], [1, 1, 1]],
            [[1, 1], [1, 1], [1, 1]],
            [[], []]
        ]
        weight2 = [
            [[0, 1, 2], [3, 4, 5]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[], []]
        ]
        weight3 = [
            [[17, 17, 17], [17, 17, 17], [17, 17, 17]],
            [[17, 17, 17], [17, 17, 17], [17, 17, 17]],
            [[], [], []]
        ]
        self.networks[0]._set_weights(weight1)
        self.networks[1]._set_weights(weight2)
        self.networks[2]._set_weights(weight3)
        self.assertEqual(self.networks[0]._get_weights(), weight1)
        self.assertEqual(self.networks[1]._get_weights(), weight2)
        self.assertEqual(self.networks[2]._get_weights(), weight3)

    def test_run_raises_index_error_with_improper_input(self):
        """Test improper input raises index error."""
        self.assertRaises(IndexError, self.networks[0].run, [1])
        self.assertRaises(IndexError, self.networks[1].run, [1])
        self.assertRaises(IndexError, self.networks[2].run, [1, 1])

    # # ============== Not used yet ==================

    # def test_run_provides_proper_output(self):
    #     """Test provides proper output."""
    #     weight1 = [
    #         [[1, 1, 1], [1, 1, 1]],
    #         [[1, 1], [1, 1], [1, 1]],
    #         [[], []]
    #     ]
    #     weight2 = [
    #         [[1, 1, 1], [1, 1, 1]],
    #         [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],
    #         [[1, 1], [1, 1], [1, 1], [1, 1]],
    #         [[], []]
    #     ]
    #     weight3 = [
    #         [[0, 0, 0], [1, 1, 1], [1, 1, 1]],
    #         [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    #         [[], [], []]
    #     ]
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

    # def test_make_node_males_a_node(self):
    #     """Test should make a new Node."""
    #     self.networks[0].make_node_males_a_node(
    #         self, layerindex, index, sizes, nodes=None
    #     )

    # def each_node(self, visitoutput, callback, *args):
    #     """."""
    #     num = 0 if visitoutput else 1
    #     lastlayer = len(self.layers) - num
    #     for i in range(lastlayer):
    #         # print('-------------------------------')
    #         # print('now in layer', i)
    #         for j in range(len(self.nodes[i])):
    #             callback(self.nodes[i][j], i, j, self.nodes, *args)

    # # ================== End ================

    def test_net_creates_network_with_sizes(self):
        """Test net works with sizes."""
        test_net = Neural([1, 1, 1])
        for layer in test_net.layers:
            for node in layer:
                self.assertTrue(node.input == 0)
        # import pdb; pdb.set_trace()

    def test_net_creates_network_with_nodes(self):
        """Test net works with sizes."""
        test_net = Neural([1, 1, 1])
        test_net2 = Neural(test_net.layers)
        for layer in test_net2.layers:
            for node in layer:
                self.assertTrue(node.input == 0)

    # def _get_thresholds(self):
    #     """Find the thresholds."""
    #     to_return = []
    #     for i in range(len(self.nodes)):
    #         to_return.append([])
    #         for j in range(len(self.nodes[i])):
    #             try:
    #                 to_return[i].append(self.nodes[i][j].threshold)
    #             except Exception:  # Need more specific
    #                 to_return[i].append(0)
    #     return to_return
    #
    # def _set_thresholds(self, thresholds):
    #     """Set thresholds."""
    #     self.each_node(False, self._set_thresholds_callback, thresholds)
    #
    # def _set_thresholds_callback(
    #     self, node, layerindex, index, nodes, thresholds
    # ):
    #     """Thresholds callback."""
    #     node.threshold = thresholds[layerindex][index]
    #
    # def _set_weights_callback(self, node, layerindex, index, nodes, weights):
    #     """Set wieghts."""
    #     node.weights = weights[layerindex][index]
    #     print(weights[layerindex][index])
    #
    # def reset(self):
    #     """Reset Node."""
    #     self.each_node(True, self._reset_callback)
    #
    # def _reset_callback(self, node, layerindex, index, nodes):
    #     """Reset Node."""
    #     node.input = 0

    def test_set_inputs_changes_layer1_input_values(self):
        """Set the inputs."""
        test_net = Neural([3, 3, 3])
        test_net.set_inputs([5, 5, 5])
        for i in range(3):
            self.assertTrue(test_net.layers[0][i].input == 5)

    def test_set_inputs_to_many_raises_exception(self):
        """Set the inputs."""
        test_net = Neural([1, 1])
        self.assertRaises(IndexError, test_net.set_inputs, [5, 5, 5])

    # def run(self, inputs):
    #     """Run."""
    #     if inputs:
    #         self.set_inputs(inputs)
    #     self.each_node(False, self._run_callback)
    #     return self.get_outputs()
    #
    # def _run_callback(self, node, layerindex, index, nodes):
    #     """Run callback."""
    #     # print('+++++++++++++++')
    #     # print('node threshold', node.threshold)
    #     # print('node input', node.input)
    #     # print(layerindex, index)
    #     # print('node weights', node.weights)
    #     if node.input >= node.threshold:
    #         for i in range(len(node.weights)):
    #             # print('------')
    #  nodes[layerindex + 1][i].input += node.weights[i] * node.input
    #             # print(
    #             #     'node', i,
    #             #     'at layer', layerindex + 1,
    #             #     'now has input of', nodes[layerindex + 1][i].input
    #             # )
    #
    # def get_outputs(self):
    #     """Get outputs."""
    #     to_return = []
    #     for i in self.nodes[len(self.nodes) - 1]:
    #         to_return.append(i.input)
    #     return to_return
    #
    # def clone(self):
    #     """Clone the beast."""
    #     return Neural(self.nodes)
    #
    # def export(self):
    #     """Export data."""
    #     return {
    #         'thresholds': self._get_thresholds(),
    #         'weights': self._get_weights()
    #     }
    #
    # def _import(self, data):
    #     """Import somthing."""
    #     net = Neural(self.get_sizes(data.thresholds))
    #     net._set_thresholds(data.thresholds)
    #     net._set_weights(data.weights)
    #     return net
