"""The manipulation file for AI.py."""
from tic_tack import directory, new_board, greedy_bot
from AI import Neural, Node
from math import floor
import random



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
        # self.board = self.board[:next_board['move']] + 'O' + self.board[next_board['move'] + 1:]
        # if self.winner is True:
        #     return
        # self.history.append(self.board)

    def undo(self):
        """Undo a move."""
        # if len(self.history) > 1:
        #     self.history.pop()
        self.board = self.history.pop()
        self.winner = None
        self.turn = 'X' if self.turn == 'O' else 'O'

class Network(Neural):

    def get_inputs(self, board, turn):
        inputs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0]
        for i in range(len(board)):
            if board[i] == turn:
                inputs[i * 2] = 1
            elif board[i] == " ":
                pass
            else:
                inputs[i * 2 + 1] = 1
        return inputs

    def get_move(self, game):
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
            print('---------------------')
            print(game.board)
            output = throwaway.run(self.get_inputs(game.board, game.turn))[0]
            print(throwaway.run(self.get_inputs(game.board, game.turn)))
            if output > largest:
                largest = output
                top = [move]
            elif output == largest:
                top.append(move)
        # print(top)
        return top[0]



class Individual(object):
    """."""

    def __init__(self, id=-1, net=None):
        """."""
        self.id = id
        self.net = net
        self.age = float('-inf')
        self.score = float('-inf')
        self.AGE_MAX = 8
        self.SCORE_MAX = 4298

    def compare_to(self, other):
        """."""
        return self.compare(self, other)

    def evaluate_one(self, board_dict):
        """."""
        game = Game(board_dict['board'])
        board_list = []
        for x in game.board:
            board_list.append(x)
        if not board_dict['Right_moves']:
            board_dict['Right_moves'] = greedy_bot(board_list)
        network = (Network(self.net))
        if network.get_move(game) == board_dict['Right_moves']:
            self.score += 1
            return True
        else:
            return False

    def evaluate(self):
        """."""
        test_boards = self.generate_test_boards()
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

    def generate_test_boards(self, boards=[[] for i in range(8)],
                             visited={}, game=None):
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
            boards[9 - len(emptysquares)].append({
                'board': game.board,
                'Right_moves': None
            })
        except:
            pass
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
        dest.each_node(False, self._splice_callback(), source)

    def _splice_callback(self, node, layer_index, index, nodes, source):
        """."""
        if self.heads():
            node.threshold = source.node[layer_index][index].threshold
        for i in range(len(node.weights)):
            if self.heads():
                node.weights[i] = source.nodes[layer_index][index].weights[i]

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

    def randomize(self, net, modify_chance=0.01, min_thresh=-100, max_thresh=100, min_weight=-10, max_weight=10):
        """."""
        net.each_node(False, self._randomize_callback, modify_chance, min_thresh, max_thresh, min_weight, max_weight)
        return net

    def _randomize_callback(self, node, i, j, nodes, modify_chance, min_thresh, max_thresh, min_weight, max_weight):
        """."""
        node.threshold = self.randomize_value(node.threshold, modify_chance, min_thresh, max_thresh)
        for i in range(len(node.weights)):
            node.weights[i] = self.randomize_value(node.weights[i], modify_chance, min_weight, max_weight)

    def new_random(self, id, sizes):
        """."""
        return Individual(id, self.randomize(Neural(sizes), 1))

    def mutate(self, mutation_rate):
        """."""
        self.randomize(self.net, mutation_rate)
        return self

    def export(self):
        """."""
        return {'id': self.id, 'net': self.net.export() }

    def ind_import(self, data):
        id = data['id']
        net = Neural._import(data['net'])
        sizes = net.get_sizes()
        if len(sizes) < 1 or sizes[0] != 18 or sizes[-1] != 1:
            raise ValueError('Please import object with 18 input nodes and 1 output node.')
        return Individual(id, net)

class Generation(object):
    """Docstring for ClassName."""

    def __init__(self, individuals, id=0):
        """.""" 
        self.id = id
        self.individuals = individuals

    def run(self):
        """."""
        for individual in individuals:
            individual.evaluate()

    def order(self):
        """."""
        for i in range((len(individuals) - 1), 0, -1):
            floor()
        pass

    def select(self, pool):
        """."""
        x = random.random()
        x = x * x
        return pool[floor(x * len(pool))]

    def next(self, mutation_rate=0.05, clones=0, id=-1):
        """."""
        if id < 0:
            id = self.id + 1
        old_individuals = self.individuals
        new_individuals = []
        for i in range(clones):
            new_individuals.append(old_individuals[i].clone(len(new_individuals)))
        while len(new_individuals) < len(old_individuals):
            a = self.select(old_individuals)
            b = self.select(old_individuals)
            new_individuals.append(a.reproduce(len(new_individuals), b).mutate())
        return Generation(new_individuals, id)

    def new_random(self, size=100, sizes=[18,27,9,1], id=0, imported=[]):
        """."""
        individuals = [0 for i in range(size)]
        for i in range(len(imported)):
            individuals[i] = imported[i]
            individuals[i].id = i
        for i in range(size):
            individuals[i] = Individual().new_random(i, sizes)
        return Generation(individuals, id)

    def export(self, chunk={'index':0, 'total':1}):
        """."""
        return {
            'id': self.id,
            'individuals': list(map(lambda individual: individual.export(), self.individuals))
        }

    def gen_import(self, data):
        """."""
        id = data['id']
        individuals = data['individuals']
        return Generation(list(map(lambda individual: individual.ind_import(), self.individuals)), id)



if __name__ == "__main__":
    test = Generation([])
    test = test.new_random()
    test = test.next()
    for i in test.individuals:
        print(i.net.get_sizes(i.net.nodes))
