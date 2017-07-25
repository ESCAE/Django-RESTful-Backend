"""The manipulation file for AI.py."""
from tic_tack import directory
from AI import Neural, Node
import random


class Game(object):
    """Docstring for Game."""

    def __init__(self):
        """Make a game."""
        self.board = '         '
        self.winner = None
        self.history = []

    def emptysquares(self, board):
        """Find empty spaces."""
        empty = []
        for i in range(9):
            if board[i] == ' ':
                empty.append(i)
        return empty

    def move(self, board, move):
        """Make a move and get the response."""
        self.history.append(self.board)
        next_board = directory(board, move)
        self.board = next_board['board']
        self.winner = next_board['WL']
        # self.board = self.board[:next_board['move']] + 'O' + self.board[next_board['move'] + 1:]
        # if self.winner is True:
        #     return
        # self.history.append(self.board)

    def undo(self):
        """Undo a move."""
        # if len(self.history) > 1:
        #     self.history.pop()
        self.board = self.history.pop()


class Individual(object):
    """."""

    def __init__(self, id, net):
        """."""
        self.id = id
        self.net = net
        self.age = float('-inf')
        self.score = float('-inf')
        self.AGE_MAX = 8
        self.SCORE_MAX = 4298

    def compare_to(self, other):
        """."""
        return Genetic.compare(self, other)

    def evaluate_one(self, b):
        """."""
        # game = new Ttt.Game(b.board)
        if not b.rightMoves:
            # b.rightMoves = new Ai.Smart().getMoves(games).forEach(move)  # function (move) JS translation issue
            if b.rightMoves.index(move) >= 0:
                anyRight = True
            else:
                anyWrong = True
        if anyRight and not anyWrong:
            self.score += 1
        # return !anyWrong #JS translation issue

    def evaluate(self):
        """."""
        if not testBoards:
            generate_test_boards()
        self.score = 0
        failed_depth = -1
        # JS functions??? Needs group effort 
    #    testBoards.every(function (boards, depth) {
    #         boards.forEach(function (b) {
    #             if (!this.evaluateOne(b) && failedDepth < 0) {
    #                 failedDepth = depth;
    #             }
    #         }, this);

    #         // We go at least to boards with 3 moves to differentiate between
    #         // results at the same age.  There are 334 possible scores before
    #         // boards with 4 moves, which should be plenty for 100 individuals.
    #         return (failedDepth < 0 || depth < 3);
    #     }, this);

    #     this.age = (failedDepth < 0 ? testBoards.length : failedDepth);
    # };

    def clone(self, id):
        """."""
        return Individual(id, self.net.clone())

    def heads(self):
        """."""
        return random.random() < 0.5

    def splice(self, dest, source):
        """."""
        if dest == source:
            return
    # JS Translation issue
    #     dest.each_node(false, )
    #         if self.heads():
    #             node.threshold = source.nodes[layerIndex][index].threshold;
    #         }
    #         for (var i = 0; i < node.weights.length; ++i) {
    #             if (heads()) {
    #                 node.weights[i]
    #                     = source.nodes[layerIndex][index].weights[i]
    #                 ;
    #             }
    #         }
    #     });
    # }

    def reproduce(self, id, other):
        """."""
        child = self.clone(self.id)
        self.splice(child.net, other.net)
        return child

    def real_rand(self, minimum, maximum):
        """."""
        return random.random() * (maximum - minimum) + minimum

    def int_rand(self, minimum, maximum):
        """."""
        return floor(random.random() * (maximum - minimum + 1)) + minimum

    def randomize_value(self, v, modify_chance, min_perturb, max_perturb):
        """."""
        if random.random() < modify_chance:
            v += self.real_rand(min_perturb, max_perturb)
        return v

    def randomize(self, net, modify_chance, min_thresh, max_thresh, min_weight, max_weight):
        """."""
        try:
            modify_chance = modify_chance
        except:
            modify_chance = 0.01

        min_thresh = min_thresh or -100
        max_thresh = max_thresh or 100
        min_weight = min_weight or -10
        max_weight = max_weight or 10

        net.each_node(false)  # function (node)
        node.threshold = self.randomize_value(node.threshold, modify_chance, min_thresh, max_thresh)
        for i in range(len(node.weights)):
            node.weights[i] = randomize_value(node.weights[i]=0, modify_chance, min_weight, max_weight)
        return self.net

    def mutate(self, mutation_rate):
        """."""
        self.randomize(self.net, mutation_rate)
        return self


class Genetic(object):
    """."""

    def __init__(self):
        """."""
        pass

    def generate_test_boards(self, boards=['         ' for i in range(8)],
                             visited={}, game=None):
        """Make some test boards."""
        boards = boards
        visited = visited
        game = game if game else Game()
        # print('---')
        # print(game.winner)
        emptysquares = game.emptysquares(game.board)
        try:
            if (visited[game.board] or game.winner or game.winner is False or len(emptysquares) <= 1):
                # print(visited[game.board])
                return boards
        except:
            pass

        print(emptysquares)
        try:
            boards[9 - len(emptysquares)] = game.board
        except:
            pass
        #     'right_moves': None
        # })

        visited[game.board] = True

        for move in emptysquares:
            game.move(game.board, move)
            self.generate_test_boards(boards, visited, game)
            game.undo()

        return boards

    def compare(self, a, b):
        """Compare two individual Neurals by age or score."""
        if a.age != b.age:
            return a.age - b.age
        return a.score - b.score

    def compare_descending(self, a, b):
        """."""
        return self.compare(b, a)


class Generation(object):
    """Docstring for ClassName."""

    def __init__(self, id, individuals):
        """."""
        self.id = id or 0
        self.individuals = individuals

    def run(self):
        """."""
        for individual in individuals:
            Individual.Individual.evaluate()

    def order(self):
        """."""
        for i in range((len(individuals) - 1), 0, -1):
            floor()
        pass


if __name__ == "__main__":
    test = Genetic()
    print(test.generate_test_boards())
