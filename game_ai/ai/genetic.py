"""The manipulation file for AI.py."""
from ai.AI import Neural
from math import floor
import random
from ai.tic_tack import greedy_bot
from ai.tic_tack import new_board
from operator import attrgetter


# Found Issues
# **********************************
# 1. 214 randomize, param net is a list. list does not have the attribute
# of 'each_node'. Maybe solved with line 114.


class Game(object):
    """Docstring for Game."""

    def __init__(self, board='         '):
        """Make a game."""
        self.board = board
        self.winner = None
        self.history = []
        self.turn = 'X' if len(self.emptysquares(self.board)) % 2 == 0 else 'O'

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
        board_list = []
        for x in board:
            board_list.append(x)
        next_board = new_board(board, move, self.turn, 1)
        self.board = next_board['board']
        self.winner = next_board['WL']
        self.turn = 'X' if self.turn == 'O' else 'O'

    def undo(self):
        """Undo a move."""
        self.board = self.history.pop()
        self.winner = None
        self.turn = 'X' if self.turn == 'O' else 'O'


class Network(Neural):
    """Create Network with boards states."""

    def get_inputs(self, board, turn):
        """Get this inputs."""
        inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(board)):
            if board[i] == turn:
                inputs[i * 2] = 1
            elif board[i] == " ":
                pass
            else:
                inputs[i * 2 + 1] = 1
        return inputs

    def get_move(self, game):
        """Get a move."""
        largest = float('-inf')
        top = []
        stored_board = game.board
        stored_turn = game.turn
        throwaway = self
        for move in game.emptysquares(game.board):
            game.board = stored_board
            game.turn = stored_turn
            game.move(game.board, move)
            throwaway.reset()
            output = throwaway.run(self.get_inputs(game.board, game.turn))[0]
            game.undo()
            if output > largest:
                largest = output
                top = [move]
            elif output == largest:
                top.append(move)
        return top[0]


class Individual(object):
    """Represent a individual neural net."""

    def __init__(self, tag=-1, net=None):
        """."""
        self.tag = tag
        self.net = net
        self.age = float('-inf')
        self.score = 0
        self.AGE_MAX = 8
        self.SCORE_MAX = 4298
        self.winner = False
        self.seen_list = []

    def compare_to(self, other):
        """Referencing compare call self to a given individual."""
        return self.compare(self, other)

    def evaluate_versus(self, other):
        """."""
        game = Game()
        a = self
        b = other
        while True:
            if ' ' not in game.board:
                a.score += 1
                b.score += 1
                break
            game.move(game.board, a.net.get_move(game))
            if game.winner is not None:
                a.score += 2
                b.score -= 2
                break
            if ' ' not in game.board:
                a.score += 1
                b.score += 1
                break
            game.move(game.board, b.net.get_move(game))
            if game.winner is not None:
                b.score += 2
                a.score -= 2
                break

    def evaluate_versus_greedy_bot(self):
        """."""
        game = Game()
        a = self
        b = greedy_bot
        while True:
            if ' ' not in game.board:
                a.score += 9
                break
            game.move(game.board, a.net.get_move(game))
            if game.winner is not None:
                a.score += 20
                break
            if ' ' not in game.board:
                a.score += 9
                break
            board_list = []
            for x in game.board:
                board_list.append(x)
            game.move(game.board, b(board_list, game.turn))
            if game.winner is not None:
                a.score += 9 - game.board.count(' ')
                break
        game = Game()
        while True:
            board_list = []
            for x in game.board:
                board_list.append(x)
            game.move(game.board, b(board_list, game.turn))
            if game.winner is not None:
                a.score += 9 - game.board.count(' ')
                break
            if ' ' not in game.board:
                a.score += 9
                break
            game.move(game.board, a.net.get_move(game))
            if game.winner is not None:
                a.score += 20
                break
            if ' ' not in game.board:
                a.score += 9
                break

    def evaluate_one(self, board_dict):
        """Compare scoring function.

        that will take a game board and evaluate any
        given game move decision against Greedy Bot.
        """
        game = Game(board_dict['board'])
        if self.net.get_move(game) == board_dict['Right_moves']:
            self.score += 1
            return True
        else:
            return False

    def evaluate(self, test_boards):
        """Test non-ended condition boards against individual neural net."""
        self.score = 0
        failed_depth = -1
        filler_list = []
        for depth in range(len(test_boards)):
            for board in test_boards[depth]:
                if not self.evaluate_one(board) and failed_depth < 0:
                    failed_depth = depth
            if failed_depth < 0 or depth < 3:
                filler_list.append(True)
            else:
                filler_list.append(False)
        self.age = len(test_boards) if failed_depth < 0 else failed_depth

    def compare(self, a, b):
        """Compare two individual Neurals by age or score."""
        if a.age != b.age:
            return a.age - b.age
        return a.score - b.score

    def compare_descending(self, a, b):
        """Compare two Nets by age or score in the opposite order."""
        return self.compare(b, a)

    def clone(self, tag):
        """Clone the instance."""
        return Individual(tag, self.net)

    def heads(self):
        """Return a 50/50 True/False."""
        return random.random() < 0.5

    def splice(self, dest, source):
        """Check if the dest and source networks are the same.

        If not run a splice callback on each node of the dest network.
        """
        if dest == source:
            return dest
        new = Network(dest.layers)
        new.each_node(False, self._splice_callback, source)
        return new

    def _splice_callback(self, node, layer_index, index, nodes, source):
        """Use the heads function get a 50/50 on new thresholds and weights."""
        if self.heads():
            node.threshold = source.layers[layer_index][index].threshold
        for i in range(len(node.weights)):
            if self.heads():
                node.weights[i] = source.layers[layer_index][index].weights[i]

    def reproduce(self, tag, other):
        """Clone a given individual network from that 'child'.

        run the splice function with the child and another individual network.
        """
        new = self.splice(self.net, other.net)
        child = Individual(tag, new)
        return child

    def real_rand(self, minimum, maximum):
        """Return a rand real number with a given min and max to influence."""
        return random.random() * (maximum - minimum) + minimum

    def int_rand(self, minimum, maximum):
        """Return a random integer with a given min and max to influence."""
        return floor(random.random() * (maximum - minimum + 1)) + minimum

    def randomize_value(self, v, modify_chance, min_perturb, max_perturb):
        """."""
        if random.random() < modify_chance:
            v += self.real_rand(min_perturb, max_perturb)
        return v

    def randomize(
        self, net, modify_chance=0.01, min_thresh=-100,
        max_thresh=100, min_weight=-10, max_weight=10
    ):
        """Grab each node in a neural net and uses the randomize callback."""
        net.each_node(
            False, self._randomize_callback, modify_chance, min_thresh,
            max_thresh, min_weight, max_weight
        )
        return net

    def _randomize_callback(
        self, node, i, j, nodes, modify_chance, min_thresh,
        max_thresh, min_weight, max_weight
    ):
        """Call the randomize value for a given node's threshold and weights.

        with set min and max.
        """
        node.threshold = self.randomize_value(
            node.threshold, modify_chance, min_thresh, max_thresh
        )
        for i in range(len(node.weights)):
            node.weights[i] = self.randomize_value(
                node.weights[i], modify_chance, min_weight, max_weight
            )

    def new_random(self, tag, sizes):
        """Return New Random."""
        return Individual(tag, self.randomize(Network(sizes), 1))

    def mutate(self, mutation_rate=0.05):
        """Mutation the current instance of the Individual."""
        self.randomize(self.net, mutation_rate)
        return self

    def export(self):
        """Export a individual network, in dictionary form."""
        return {'tag': self.tag, 'net': self.net.export()}

    def ind_import(self, data):
        """."""
        tag = data['tag']
        net = Network([1, 1])
        net = Network(net._import(data['net']).layers)
        sizes = net.get_sizes(net.layers)
        if len(sizes) < 1 or sizes[0] != 18 or sizes[-1] != 1:
            raise ValueError(
                'Please import object with 18 input nodes and 1 output node.'
            )
        return Individual(tag, net)


class Generation(object):
    """Generation."""

    def __init__(self, individuals, tag=0):
        """."""
        self.tag = tag
        self.individuals = individuals
        self.test_boards = self.generate_test_boards()

    def generate_test_boards(
        self, boards=[[] for i in range(8)], visited={}, game=None
    ):
        """Make some test boards."""
        boards = boards
        visited = visited
        game = game if game else Game()
        emptysquares = game.emptysquares(game.board)
        try:
            if (visited[game.board] or game.winner or game.winner is False or len(emptysquares) <= 1):
                return boards
        except KeyError:
            if (game.winner or game.winner is False or len(emptysquares) <= 1):
                return boards
        try:
            board_list = []
            for x in game.board:
                board_list.append(x)
            correct_move = greedy_bot(board_list, game.turn)
            boards[9 - len(emptysquares)].append({
                'board': game.board,
                'Right_moves': correct_move
            })
        except Exception:  # need specific exception
            pass
        visited[game.board] = True

        for move in emptysquares:
            game.move(game.board, move)
            self.generate_test_boards(boards, visited, game)
            game.undo()
        return boards

    def run_versus_self(self):
        """."""
        for a in self.individuals:
            for b in self.individuals:
                if a != b and a not in b.seen_list and b not in a.seen_list:
                    a.evaluate_versus(b)
                    b.evaluate_versus(a)
                    a.seen_list.append(b)
                    b.seen_list.append(a)

    def run_versus_greedy_bot(self):
        """."""
        for i in range(len(self.individuals)):
            print(i)
            self.individuals[i].evaluate_versus_greedy_bot()

    def run(self):
        """Run evaluate for every individual network in a Generation."""
        # print('running generation', self.tag)
        self.test_boards = self.generate_test_boards()
        for individual in self.individuals:
            individual.evaluate(self.test_boards)
            print('---------')
            print('Network ID:', individual.tag)
            print('Network Score:', individual.score)
            print('Network Age:', individual.age)

    def order(self):
        """."""
        for i in range((len(self.individuals) - 1), 0, -1):
            floor()
        pass

    def select(self, pool):
        """."""
        x = random.random()
        x = x * x
        return pool[floor(x * len(pool))]

    def next(self, mutation_rate=0.05, clones=0, tag=-1):
        """."""
        self.individuals = sorted(self.individuals, key=attrgetter('age', 'score'))[::-1]
        # print('+++++++++++++')
        # print('Generation: ', self.tag)
        # print('High Score:', self.individuals[0].score)
        # print('Generation average Score:', sum(ind.score for ind in self.individuals)/(len(self.individuals)))
        # print('Generation average age:', sum(ind.age for ind in self.individuals)/(len(self.individuals)))
        # print('+++++++++++++')
        if tag < 0:
            tag = self.tag + 1
        try:
            old_individuals = self.individuals
            new_individuals = []
            for i in range(clones):
                new_individuals.append(
                    old_individuals[i].clone(len(new_individuals))
                )
            age_one = self.individuals[0]
            age_two = self.individuals[1]
            high_scores = sorted(self.individuals, key=attrgetter('score'))[::-1]
            score_two = None
            if age_one != high_scores[0] and age_two != high_scores[0]:
                score_one = high_scores[0]
            elif age_one != high_scores[1] and age_two != high_scores[1]:
                score_one = high_scores[1]
            else:
                score_one = high_scores[2]
            if age_one != high_scores[1] and age_two != high_scores[1] and score_one != high_scores[1]:
                score_two = high_scores[1]
            elif age_one != high_scores[2] and age_two != high_scores[2] and score_one != high_scores[2]:
                score_two = high_scores[2]
            else:
                score_two = high_scores[3]
            new_individuals.append(age_one)
            new_individuals.append(age_two)
            new_individuals.append(score_one)
            new_individuals.append(score_two)
            parents = [age_one, age_two, score_one, score_two]
            while len(new_individuals) < len(old_individuals):
                idx = random.randint(0, 3)
                new = parents[idx].reproduce(len(new_individuals), parents[idx - 1]).mutate(mutation_rate)
                new_individuals.append(new)
            return Generation(new_individuals, tag)
        except IndexError:
            return ('Must provide at least 4 individuals to next.')

    def new_random(self, size=100, sizes=[18, 27, 9, 1], tag=0, imported=[]):
        """."""
        individuals = [0 for i in range(size)]
        for i in range(len(imported)):
            individuals[i] = imported[i]
            individuals[i].tag = i
        for i in range(size):
            individuals[i] = Individual().new_random(i, sizes)
        return Generation(individuals, tag)

    def export(self, chunk={'index': 0, 'total': 1}):
        """."""
        return {
            'tag': self.tag,
            'individuals': list(
                map(lambda individual: individual.export(), self.individuals)
            )
        }

    def gen_import(self, data):
        """."""
        tag = data['tag']
        individuals = list(map(
            lambda individual: self.individuals[0].ind_import(individual),
            data['individuals']
        ))
        return Generation(individuals, tag)


if __name__ == "__main__":  # pragma: no cover
    """."""
    import pickle
    test = Generation([])
    test = test.new_random(20)
    for i in test.individuals:
        print(i.age)
        while i.age != 8:
            test.run()
            test = test.next(.65, 5)
    with open('testpickle', 'wb') as fp:
        pickle.dump(test.export(), fp)
    with open('testpickle', 'rb') as fp:
        imported = test.gen_import(pickle.load(fp))
    game = Game()
    a = imported.individuals[0]
    b = imported.individuals[1]
    while True:
        if ' ' not in game.board:
            break
        game.move(game.board, a.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            a.score += 1
            break
        if ' ' not in game.board:
            break
        game.move(game.board, b.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            b.score += 1
            break
    game = Game()
    a = test.individuals[1]
    b = test.individuals[0]
    while True:
        if ' ' not in game.board:
            break
        game.move(game.board, a.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            a.score += 1
            break
        if ' ' not in game.board:
            break
        game.move(game.board, b.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            b.score += 1
            break
