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

    def test_net_creates_network_with_sizes(self):
        """Test net works with sizes."""
        test_net = Neural([1, 1, 1])
        for layer in test_net.layers:
            for node in layer:
                self.assertTrue(node.input == 0)

    def test_net_creates_network_with_nodes(self):
        """Test net works with sizes."""
        test_net = Neural([1, 1, 1])
        test_net2 = Neural(test_net.layers)
        for layer in test_net2.layers:
            for node in layer:
                self.assertTrue(node.input == 0)

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

    def test_get_outputs_gets_the_outputs(self):
        """Get outputs."""
        net = self.networks[0]
        weight1 = [
            [[1, 1, 1], [1, 1, 1]],
            [[1, 1], [1, 1], [1, 1]],
            [[], []]
        ]
        net._set_weights(weight1)
        test = net.get_outputs()
        self.assertTrue(test == [0, 0])

    def test_run_raises_index_error_with_improper_input(self):
        """Test improper input raises index error."""
        self.assertRaises(IndexError, self.networks[0].run, [1])
        self.assertRaises(IndexError, self.networks[1].run, [1])
        self.assertRaises(IndexError, self.networks[2].run, [1, 1])

    def test_export_eports_the_network(self):
        """Export the network."""
        net = Neural([1, 3, 2])
        data = net.export()
        self.assertTrue(
            data == {
                'thresholds': [[1], [1, 1, 1], [0, 0]],
                'weights': [
                    [[0, 0, 0]], [[0, 0], [0, 0], [0, 0]],
                    [[], []]
                ]
            }
        )

    def test_import_imports_values(self):
        """Import somthing."""
        net = Neural([1, 1, 1])
        data = net.export()
        net2 = net._import(data)
        for i in range(len(net.layers) - 1):
            for j in range(len(net.layers[i])):
                self.assertTrue(
                    net.layers[i][j].input == net2.layers[i][j].input
                )
                self.assertTrue(
                    net.layers[i][j].threshold == net2.layers[i][j].threshold
                )
                self.assertTrue(
                    net.layers[i][j].weights == net2.layers[i][j].weights
                )

    def test_clone_clones_the_neural_net(self):
        """Test clones."""
        net = Neural([5, 6, 5])
        net2 = net.clone()
        for i in range(len(net.layers) - 1):
            for j in range(len(net.layers[i])):
                self.assertTrue(
                    net.layers[i][j].input == net2.layers[i][j].input
                )
                self.assertTrue(
                    net.layers[i][j].threshold == net2.layers[i][j].threshold
                )
                self.assertTrue(
                    net.layers[i][j].weights == net2.layers[i][j].weights
                )

    def test_rest_rests_inputs_to_zero(self):
        """Test rest restes values to zero."""
        net = Neural([2, 2, 1])
        net.run([2, 2])
        for node in net.layers[0]:
            self.assertEqual(node.input, 2)
        net.reset()
        for node in net.layers[0]:
            self.assertEqual(node.input, 0)

    def test_instanciate_a_neural_net_with_layers(self):
        """Test can create clone."""
        net = Neural([1, 1, 1])
        net2 = Neural(net.layers)
        self.assertTrue(net is not net2)
        self.assertEqual(len(net.layers), len(net2.layers))
