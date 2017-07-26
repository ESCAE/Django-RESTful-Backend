"""Neural network code."""


class Node(object):
    """New Neural Node."""

    def __init__(self):
        """Init the node."""
        self.input = 0


class Neural(object):
    """Neural Net Class."""

    def __init__(self, sizesornodes):
        """Init the net."""
        self.layers = []
        self.net(sizesornodes)

    def net(self, sizesornodes):
        """Create net with sizes or list."""
        sizes = []
        layers = []
        if type(sizesornodes[0]) == list:
            sizes = self.get_sizes(sizesornodes)
            layers = sizesornodes
        else:
            sizes = sizesornodes
        for i in range(len(sizes)):
            self.layers.append([])
            for j in range(sizes[i]):
                self.layers[i].append(self.make_node(i, j, sizes, layers))

    def get_sizes(self, nodes):
        """Return the amount of nodes in each layer."""
        return list(map(lambda x: len(x), nodes))

    def make_node(self, layerindex, nodeindex, sizes, layers=None):
        """Make a new Node."""
        node = Node()
        if layerindex < len(sizes) - 1:
            try:
                node.threshold = layers[layerindex][nodeindex].threshold
            except (IndexError, AttributeError):
                node.threshold = 1
            try:
                node.weights = list(
                    map(lambda x: x, layers[layerindex][nodeindex].weights)
                )
            except (IndexError, AttributeError):
                node.weights = [0 for i in range(sizes[layerindex + 1])]
        return node

    def run(self, inputs):
        """Set inputs(or not), return Outputs."""
        if inputs:
            self.set_inputs(inputs)
        self.each_node(False, self._run_callback)
        return self.get_outputs()

    def set_inputs(self, inputs):
        """Set the inputs."""
        if len(inputs) is not len(self.layers[0]):
            raise IndexError("To many or to few inputs for first layer!")
        for i in range(len(inputs)):
            self.layers[0][i].input = inputs[i]

    def each_node(self, visitoutput, callback, *args):
        """."""
        num = 0 if visitoutput else 1
        lastlayer = len(self.layers) - num
        for i in range(lastlayer):
            # print('-------------------------------')
            # print('now in layer', i)
            for j in range(len(self.layers[i])):
                callback(self.layers[i][j], i, j, self.layers, *args)

    def _run_callback(self, node, layerindex, index, nodes):
        """Run callback."""
        # print('+++++++++++++++')
        # print('node threshold', node.threshold)
        # print('node input', node.input)
        # print(layerindex, index)
        # print('node weights', node.weights)
        if node.input >= node.threshold:
            for i in range(len(node.weights)):
                # print('------')
                nodes[layerindex + 1][i].input += node.weights[i] * node.input
                # print(
                #     'node', i,
                #     'at layer', layerindex + 1,
                #     'now has input of', nodes[layerindex + 1][i].input
                # )

    def get_outputs(self):
        """Get outputs."""
        outputs = []
        for node in self.layers[-1]:
            outputs.append(node.input)
        return outputs

    # =============  Export related ========== #

    def export(self):
        """Export data."""
        return {
            'thresholds': self._get_thresholds(),
            'weights': self._get_weights()
        }

    def _get_weights(self):
        """Weigh the nodes."""
        weights = []
        for i in range(len(self.layers)):
            weights.append([])
            for j in range(len(self.layers[i])):
                try:
                    weights[i].append(self.layers[i][j].weights)
                except Exception:  # Need more specific exception handling.
                    weights[i].append([])
        return weights

    def _get_thresholds(self):
        """Find the thresholds."""
        thresholds = []
        for i in range(len(self.layers)):
            thresholds.append([])
            for j in range(len(self.layers[i])):
                try:
                    thresholds[i].append(self.layers[i][j].threshold)
                except Exception:  # Need more specific
                    thresholds[i].append(0)
        return thresholds

    # =========== import related ============ #

    def _import(self, data):
        net = Neural(self.get_sizes(data['thresholds']))
        net._set_thresholds(data['thresholds'])
        net._set_weights(data['weights'])
        return net

    def _set_thresholds(self, thresholds):
        """Set thresholds."""
        self.each_node(False, self._set_thresholds_callback, thresholds)

    def _set_thresholds_callback(
        self, node, layerindex, index, nodes, thresholds
    ):
        """Thresholds callback."""
        node.threshold = thresholds[layerindex][index]

    def _set_weights(self, weights):
        """Set weight."""
        self.each_node(False, self._set_weights_callback, weights)

    def _set_weights_callback(self, node, layerindex, index, nodes, weights):
        """Set wieghts."""
        node.weights = weights[layerindex][index]
        # print(weights[layerindex][index])

    # ========== reset related =========== #

    def reset(self):
        """Reset Node."""
        self.each_node(True, self._reset_callback)

    def _reset_callback(self, node, layerindex, index, nodes):
        """Reset Node."""
        node.input = 0

    # ============ clone ================== #

    def clone(self):
        """Clone the beast."""
        return Neural(self.layers)


if __name__ == '__main__':
    test = Neural([2, 3, 2])
    print(test.run([3, 3]))
