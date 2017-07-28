"""The manipulation file for AI.py."""
from AI import Neural
from math import floor
import random
from tic_tack import greedy_bot
from tic_tack import new_board
from operator import attrgetter
import pickle
from os import path


class Game(object):
    """Docstring for Game."""

    def __init__(self, board='         '):
        """Make a game."""
        self.board = board
        self.winner = None
        self.history = []
        self.turn = 'O' if len(self.emptysquares(self.board)) % 2 == 0 else 'X'

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

    def _import(self, data):
        """."""
        net = Network(self.get_sizes(data['thresholds']))
        net._set_thresholds(data['thresholds'])
        net._set_weights(data['weights'])
        return net

    def get_inputs(self, board, turn):
        """Get this inputs."""
        inputs = [0] * 18
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
        self.success = 0
        self.AGE_MAX = 8
        self.SCORE_MAX = 4298
        self.winner = False
        self.seen_list = []

    def compare_to(self, other):
        """Referencing compare call self to a given individual."""
        return self.compare(self, other)

    def evaluate_vs_every_possibility(self, board='         ',
                                      player_one=True,
                                      player_two=True):
        """."""
        game = Game(board)
        if player_one is True:
            if ' ' not in game.board:
                self.score += 5
            else:
                game.move(game.board, self.net.get_move(game))
                if game.winner is not None:
                    self.score += 10
                elif ' ' not in game.board:
                    self.score += 5
                else:
                    for move in game.emptysquares(game.board):
                        game.move(game.board, move)
                        if game.winner is not None:
                            self.score -= 10
                            game.undo()
                        else:
                            self.evaluate_vs_every_possibility(game.board,
                                                               True,
                                                               False)
                            game.undo()
        if player_two is True:
            if ' ' not in game.board:
                self.score += 10
            else:
                for move in game.emptysquares(game.board):
                    game.move(game.board, move)
                    if game.winner is not None:
                        self.score -= 5
                        game.undo()
                    elif ' ' not in game.board:
                        self.score += 10
                        game.undo()
                    else:
                        game.move(game.board, self.net.get_move(game))
                        if game.winner is not None:
                            self.score += 15
                        else:
                            self.evaluate_vs_every_possibility(game.board,
                                                               False,
                                                               True)

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
                b.score -= 5
                break
            if ' ' not in game.board:
                a.score += 1
                b.score += 1
                break
            game.move(game.board, b.net.get_move(game))
            if game.winner is not None:
                b.score += 2
                a.score -= 5
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
        yes = 0
        no = 0
        for depth in range(len(test_boards)):
            for board in test_boards[depth]:
                if not self.evaluate_one(board) and failed_depth < 0:
                    failed_depth = depth
            if failed_depth < 0 or depth < 3:
                filler_list.append(True)
            else:
                filler_list.append(False)
        self.age = len(test_boards) if failed_depth < 0 else failed_depth
        if self.age >= 2:
            for board in test_boards[1]:
                game = Game(board['board'])
                if self.net.get_move(game) == board['Right_moves']:
                    print('used move with success:', self.net.get_move(game))
                    print('---')
                else:
                    print('used move unsuccessfully:', self.net.get_move(game))
                    print('The best move was:', board['Right_moves'])
                    print('---')
            for board in test_boards[2]:
                game = Game(board['board'])
                if self.net.get_move(game) == board['Right_moves']:
                    yes += 1
                else:
                    no += 1
            print('successes:', yes)
            print('wrong:', no)
            print('-----')
        return yes

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
            try:
                node.threshold = source.layers[layer_index][index].threshold
            except IndexError:
                    pass

        for i in range(len(node.weights)):
            if self.heads():
                try:
                    node.weights[i] = source.layers[layer_index][index].weights[i]
                except IndexError:
                    pass

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
        """Return a new random value."""
        if random.random() < modify_chance:
            v += self.real_rand(min_perturb, max_perturb)
        return v

    def new_randomize(self, net, modify_chance=0.01,
                      min_thresh=-100, max_thresh=100,
                      min_weight=-10, max_weight=10):
        """."""
        if random.random() <= 0.10:
            old_dict = net.export()
            old_dict['thresholds'].insert(-2, [0] * 9)
            for i in range(len(old_dict['weights'][-2])):
                old_dict['weights'][-2][i] = [0] * len(old_dict['thresholds'][-2])
            net = Network()._import(old_dict)
        elif random.random() <= 0.10:
            if len(net.layers) > 4:
                old_dict = net.export()
                del old_dict['thresholds'][-2]
                del old_dict['weights'][-2]
                net = Network()._import(old_dict)
        new = Network(net.layers)
        new.each_node(False, self._randomize_callback, modify_chance,
                      min_thresh, max_thresh, min_weight, max_weight)
        return new

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
        self.net = self.new_randomize(self.net, mutation_rate)
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
        """Init for generations."""
        self.tag = tag
        self.individuals = individuals

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

    def run_versus_ever_possibility(self):
        """."""
        for individual in self.individuals:
            individual.evaluate_vs_every_possibility()

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
            self.individuals[i].evaluate_versus_greedy_bot()
            # print(self.individuals[i].score)

    def run(self):
        """Run evaluate for every individual network in a Generation."""
        self.test_boards = self.generate_test_boards()

        # print('running generation', self.tag)

        for individual in self.individuals:
            individual.success = individual.evaluate(self.test_boards)
            # print('---------')
            # print('Network ID:', individual.tag)
            # print('Network Score:', individual.score)
            # print('Network Age:', individual.age)
            # print('weights:', individual.net._get_weights())

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
        old_best = self.individuals[0]
        self.individuals = sorted(self.individuals,
                                  key=attrgetter('age', 'score'))[::-1]
        # print('+++++++++++++')
        # print('Generation: ', self.tag)
        # print('High Score:', self.individuals[0].score)
        # print('Old best still best:', old_best == self.individuals[0])
        # print('Generation average Score:',
        #       sum(ind.score for ind in self.individuals) / (len(self.individuals)))
        # print('Generation average age:',
        #       sum(ind.age for ind in self.individuals) / (len(self.individuals)))
        # print('+++++++++++++')
        if tag < 0:
            tag = self.tag + 1
        old_individuals = self.individuals
        new_individuals = []
        for i in range(clones):
            new_individuals.append(
                old_individuals[i].clone(len(new_individuals))
            )
        while len(new_individuals) < len(old_individuals):
            a = self.select(old_individuals)
            b = self.select(old_individuals)
            if a != b:
                new = a.reproduce(len(new_individuals),
                                  b).mutate(mutation_rate)
                new_individuals.append(new)
        return Generation(new_individuals, tag)

    def next_under_greedybot(self, mutation_rate=0.05, tag=-1):
        """."""
        for individual in self.individuals:
            if individual.success == 0 and individual.age == 1:
                individual.success = 1
        self.individuals = sorted(self.individuals,
                                  key=attrgetter('success', 'score'))[::-1]
        # print('+++++++++++++')
        # print('Generation: ', self.tag)
        # print('Oldest High Score:', self.individuals[0].score)
        # print('Generation average Score:',
        #       sum(ind.score for ind in self.individuals) / (len(self.individuals)))
        # print('Generation average age:',
        #       sum(ind.age for ind in self.individuals) / (len(self.individuals)))
        # print('+++++++++++++')
        if tag < 0:
            tag = self.tag + 1
        try:
            old_individuals = self.individuals
            new_individuals = []
            new_individuals.append(self.individuals[0].clone(len(new_individuals)))
            new_individuals.append(self.individuals[1].clone(len(new_individuals)))
            new_individuals.append(self.individuals[2].clone(len(new_individuals)))
            parents = new_individuals
            while len(new_individuals) < len(old_individuals):
                a = self.select(parents)
                b = self.select(parents)
                if a != b:
                    new = a.reproduce(len(new_individuals),
                                      b).mutate(mutation_rate)
                    new_individuals.append(new)
            return Generation(new_individuals, tag)
        except IndexError:
            raise IndexError('Must provide at least 3 individuals to next.')

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

path_to_pickle = path.realpath(__file__).replace('genetic.py', 'testpickle')


def move(board, move):
    """Make a move based on a neural net."""
    board_dic = new_board(board, move)
    if board_dic['WL'] is not None:
        return board_dic
    # with open(path_to_pickle, 'rb') as fp:
    #     neural = pickle.load(fp)
    neural = {'tag': 0, 'net': {'thresholds': [[-172.66250719684888, 443.64826873819914, -828.1074688820008, -788.2895159488619, -1107.0314452898017, -598.9258198909802, 189.01690149407762, -401.21654090916763, 288.8718759290207, -58.027982938813295, 647.3022930713526, -17.64498333429117, -32.18302311614557, 838.2452340986652, -440.4700426405685, -388.55169251754705, -470.76277944131033, 452.1399139181725], [-1117.8366904103418, 761.798584345622, -410.223910919946, -150.45281194901065, 208.43939900900375, 538.5148364618528, -715.202607503955, 173.54543687814981, -62.93711813645719, 516.2528094939512, -621.6973463099501, 39.38688595228561, 517.982326468133, 748.2753284798266, -490.6800740924746, -33.20564513961191, -660.9836838888137, -436.73350334313636, 128.70574643569734, -900.1127448785604, 58.34209083812135, 112.2299588936586, 327.74096621151295, 538.235385566658, 176.73779637624455, 325.8979415630255, 1139.2524635656328], [900.2884172465233, -430.78276988586356, 798.4423331181239, 251.57393955581747, -672.1584785344179, -1123.257483774197, 449.7200228796587, -310.52139766541853, -133.98616005904518], [0]], 'weights': [[[85.39096133255563, 42.00009980962105, 34.65184410538488, 5.953934013797079, -20.294244079263223, -47.418783795716294, 2.86788839334132, 94.3479012626189, -39.705033287420335, 81.36617218299578, -41.35414452676401, 167.8508026519851, 49.331092547590224, 40.90694423347376, -63.80597940348113, 41.81230678616153, -34.97485446023801, 75.69096630253196, 26.320474976248008, 10.82415815798636, 72.6025830720641, 80.89976354466297, -53.85035520622592, 6.306413912648917, -4.9369335773795235, 70.38469999293127, 47.25861271109132], [-11.9823430306291, 9.457462404476278, 24.186202302472186, -1.5478124177971697, 107.1133363338212, 23.42912938525005, 50.90310059743327, 114.06736944666696, -29.068876749024454, 82.57827603427822, -25.12992299971002, -19.878465465439888, -9.728954675666618, -39.57517719301059, -7.102478230532062, -45.43937582686932, -20.033919095413154, -47.40737274228158, -49.94213898885651, 47.41270712812382, 10.200230761301407, 53.056555670169445, -70.4161085334119, 49.26562998621041, 44.728446855849185, 2.4157315849417955, 89.54733456607558], [45.387673191906316, -89.01165074456827, -49.44050779415485, -12.651512879051069, -49.014010830427324, 77.70333928138864, 5.129085495081342, -47.42115130739502, 20.841078168344314, 18.30746684830695, -27.47625497912395, 19.484914773017245, -62.78719829988035, -120.22320711326303, -48.22464511984557, -15.779555489673218, 40.985349985104726, 8.557469648670706, -35.9286206462391, 52.612278927496355, 17.650729946159068, 44.680989516151556, -60.80587276230281, 9.255231596499511, -12.440557272130054, 119.30802246131105, 31.990949033668873], [-61.89590194312099, 4.9364907727562155, -25.184520988243882, -67.9475148651802, -43.37186716545262, -83.86413681714387, 3.6302711903917455, -50.81217010319021, 23.919817328384397, 56.27040754669409, -24.2501477416356, -105.44938793462134, 40.2571067223729, 101.88084222673577, 11.434583092176839, -123.38750183482058, 5.884126127872484, -55.91267943495143, 8.709900412890772, 44.618674803217296, -1.312852311128811, 34.60418709464539, 0.7731260873223738, 29.420120475972205, 56.304569856393684, -12.70870823570036, 52.37278659999125], [56.08651632636425, -127.0385811401825, 39.97377774575906, 35.56144057358752, 33.575805158656806, -34.76288127072563, 35.32035014925319, 5.501673933929027, 104.39900489959639, 33.63804018104362, 10.46311070835377, 79.87573557719399, -32.87592782605309, -10.849009853228246, -30.800945069723355, 59.01995606550489, 72.392936071783, 38.222323606822364, -73.775871526056, 53.174436966286144, -59.02988076363684, 57.81319507699913, -97.3346067768325, 54.33088572128882, -18.962589806728893, 36.84514876169848, -15.57462795468052], [-157.8877463025845, 41.4413353459281, 31.949000558296614, 49.61755853663698, 20.787589281045243, -9.828563937886122, 28.397260099990945, -24.942109766850415, 77.295632874396, -32.9661863922547, 37.09334684955788, 16.686674742701086, -17.361188980307652, 59.65989778002429, -113.07148711182954, -110.9824310886448, 46.08380892274212, 16.24645785273297, -0.6583524371815326, -59.83541894180627, -4.614051118731677, 0.0792877980387594, 15.647816148055218, 23.04185888564687, -20.406481607484363, -33.26464091375583, -74.9190943681125], [102.8266960683269, 5.7130534837472595, 23.74656845084879, -20.59071928800794, 67.4498581617829, 31.626619381350885, 31.10977390987602, -30.21229316487061, -118.98677881158866, -4.2221652744775735, -32.8058187362357, 23.279339692870458, 35.078050271163086, -90.83756541498265, 11.111961728128366, 22.763667177741304, 88.3838299638315, -134.95061197740674, -45.21652695362212, -29.769715317537543, -16.769336967839372, 34.382008938249115, -18.42386352868284, -9.366831500188278, -0.7115364314659471, -46.025412393967294, -40.44053546524456], [-87.30150414861144, 71.28936081579894, 67.71548630930864, -21.292145472397014, -15.184722012312768, -54.68571587220855, 67.77658623767749, -55.45045396471006, -73.05205893390237, 24.22846791212901, -19.62687908454719, 54.979154373920565, 31.19548126904904, -20.62080641340573, 124.57530483292484, 23.22439049424549, 21.865645202105092, 108.8696857542389, -19.118553439875352, 49.59509236362311, -64.90752348905647, 123.63844266207401, -89.57147592213059, -88.42556646247498, -11.990666335431534, -66.30353818733741, 8.265264069366943], [-43.01009084446741, 7.068425563284656, 104.66652350776161, 102.32431362419912, 73.86323935021942, 66.83710869113074, 41.69863437047693, -80.3492948061704, -54.9217992706298, -33.731008871258524, -31.837359629214568, -45.10551058680562, 21.759725017518022, -17.199763782293697, 14.17048612696503, 8.657954493514909, 89.31609613217627, 12.646658320054549, 19.322398171716557, -70.88501037964132, -17.51419323344893, -39.186077385479564, 47.16607383319444, 23.924228491783104, -4.453444000096088, -91.71913533263378, -59.602171200953606], [8.391925596855156, -91.890482296464, 74.61129978907641, 36.315467954656135, -52.40150444787892, -55.282432081292754, -46.79309457745913, 2.4506811497400047, 61.73586809301213, -21.54693550239262, -35.579056054223734, 64.65027804098915, 127.63706430460718, -66.5856632443433, -32.54148475412244, -47.656480145927304, 34.239481981969604, -32.16107129722325, 65.21256307968358, 24.049805811309618, -20.50651412971127, 103.25012103917747, -21.746186983325995, 59.61524683314063, -73.05786704899671, -0.6995826208441702, -19.949251027527637], [-41.81675754626004, 13.783870407015234, 15.784138784697035, 40.99027841905106, -27.59347640555898, -29.696437874717546, 26.07462915493949, 94.59570240133081, -7.839376114319769, -14.271576767286692, 55.67519714553093, 58.33587701017561, -51.00161256881705, 55.88998223748574, 1.8346147967337956, -18.05317970925901, -78.09602466858, 29.74276980104043, -47.41410965572216, -15.467806070594825, -50.55315693351742, -2.4843474743637977, 177.79590031591025, 159.45163949408948, -78.29331064411599, 62.11869574130225, 4.479030238441815], [-139.41080525197376, -22.173725248985388, -26.044064404636956, 4.4708716690852395, -35.6676952643571, 24.67989061561108, 46.06063733298034, -123.26899160973014, 166.26679355899475, 22.38747319004826, -19.312908830851278, 10.521887399532309, 22.307911175745552, 59.811653313420585, 25.417206995215246, -90.76116210679068, 46.67920550797198, 70.17448126590499, -39.003623257942444, -59.536299760589436, 17.87926325766587, 20.067343807566477, 21.168687405298936, -85.7085085108358, 33.18597303833961, 97.65702517162251, 53.180266582973786], [-11.216255006213636, 20.591213058143545, -58.73009798390544, 26.369635061815195, -101.10512169134198, 34.498283861065076, 16.775347277255847, 29.475802376024646, 42.290977775637515, -73.49932741549645, -47.05142374385714, 96.18417402038617, 21.22072472883284, -24.734303629125677, 143.60460968789843, -16.986310587826512, -31.6088614280076, -7.234593198223761, -9.430080248662668, 51.38303964213959, -9.561636004778665, 126.60369521149221, 48.619061811520226, -18.695584983141142, -20.45565129406495, -79.48218104037363, 14.495443342148132], [17.112269353429163, 79.09809698796583, -21.58650162048697, -5.106345715346816, -6.845930475893807, 44.19424308341023, 37.625196078073856, 43.56126481532585, -52.37936308622538, -42.137676125716, 41.92272983125132, -6.662083975349733, -24.481400539363957, -14.18951427520323, -9.595619478492445, -4.05472920633127, 156.59193914047006, 13.372548750738625, -8.05540807067045, 34.894844913497415, 56.20375705463037, 29.39473527538764, 52.09851298319086, 18.346447046158353, 66.89749042386063, 10.303484438051395, 30.760760970865068], [-62.25742134062086, 37.37800936884146, -23.435665919811164, 48.88714533227605, -91.60411631312896, 100.12290890474036, -46.03816673267136, -86.6057097882129, -32.576263278566685, -18.77165216159639, 60.99595420418923, -30.832350141704236, 12.933365074727353, 7.903835190381857, 97.88205102975576, 106.05718297492402, 6.573049365628491, -19.17946294191709, -29.466618814183597, -39.69971673545443, 83.96492714832328, 0.2827957308850575, -12.542746223892301, -45.219554185504634, -110.78466819825115, 59.73379954870902, -14.863700040725298], [97.37832689828141, -42.07365551324061, 2.3060171663695783, -7.31549506981262, 109.93130447015231, -49.29480313322989, 56.674217536017, 54.5178157795498, 30.271311190630662, -0.572534472077372, -83.48776572240982, 8.041437277647209, -68.8241348729321, -33.130905901375016, -26.306691353883192, 28.789279482466455, 0.7630228826666707, 95.19221126284918, -66.54777080217845, -36.00144350253566, -71.94541882309211, -21.249928933649255, 10.026624892591864, -2.2168764654787143, 0.689890907097439, 47.23454570807881, -53.47948011110955], [-77.64540484338005, 49.93438172843045, 94.29081240978374, 9.268556638118877, 14.131396983604157, -6.757535870539825, -57.19307857748882, -13.543885183501823, 49.09833880158021, 29.34741329478677, 33.0676096139823, 41.304706900801975, 60.109427928238, -25.242987965119568, -39.83111043330095, 129.6403733506732, 28.442767369285882, -3.9877622488524995, 64.13816499193236, 30.395348131203654, -24.138542163838196, 111.34616617688494, -33.231344974095705, -19.47230859458181, -10.08193984617057, 10.210635741825843, 88.74595003027315], [-38.33577961373718, -74.60748994246197, -109.32343784582758, 25.76451351399679, -8.725700154061752, -109.2097174556243, 71.74843397077174, 96.40544756385579, 55.3005872314488, -46.94217449478171, -9.424846322520349, 50.79432914775868, 43.596112929995364, -78.65930465675613, 50.72834824768219, -22.765847403698437, -70.21852711289608, 66.31625778761708, -39.225918159457464, -141.87105079882767, 17.28705385188357, -93.8594854844751, -80.233458480113, -106.62572798160443, 62.108893742160625, 90.72706107229803, -18.28152131028761]], [[38.37585251590346, -33.46080506585393, -44.05879551854047, -41.60411857242589, -22.052427659205915, 23.787969489577083, -51.11423600277267, -79.89342841428453, 19.739718089122203], [85.3220419857394, -25.39183560559389, 72.52027961705389, 55.47452443956243, 23.63864211402675, 25.5768599958254, -58.45506652913948, -101.53127828602913, 51.6554673502476], [-39.421467910823296, 20.56035260001148, 14.657103640981711, 59.697361391779836, -56.338060009558234, 25.93119119737132, -21.528230192389383, 85.79627826837341, 120.75214081465606], [42.190214839534924, 78.77809216919759, -99.97376733933976, -123.19446527626097, 27.026801844608777, 14.109395607261487, -92.59909788175177, 18.7462292862728, -97.14629666540114], [65.29394759465501, 4.6872877712619445, 11.952370141243332, 2.4456139453397423, -23.198131446549734, 84.09227290544808, 19.918972575190548, 70.35258398300377, -87.61040231493402], [-54.51938110991698, 93.4377643962182, -6.679883948930742, 32.81052363574157, -103.87120789341792, -44.319490059783966, 22.501879920899484, -97.6107274743973, 32.742992334761155], [73.6885690352241, 40.99280830017693, 48.4024554195052, 30.35237094879655, -60.647516844330084, 63.902469004712756, 11.991948552391067, 182.75753542098587, 15.311668529269467], [-0.22391179708143127, 107.09874333060539, 19.82298493296011, -13.710178597739718, 72.3969035498079, 40.42315568966165, -43.22359684067956, -45.11433275829923, 141.59992723250426], [36.830037198263526, 22.72672868037966, -66.9486175320119, -64.4066886576271, 69.26367059667683, 38.67559450864081, -46.95039358912385, -50.79289749827027, 4.432252541292437], [-134.8809947299261, -63.812769020919895, -43.24847165091661, 27.445505188870637, 13.466297473129314, 87.1748768886564, 25.272241722087855, -44.767159504477036, 12.436086878244701], [87.40160898692642, 40.3999208915452, 8.738177828382751, 9.789828336932025, 32.403913097426724, 11.525191064261247, 12.891957199389479, 2.5501546257228185, -23.35415920982888], [-46.869155535707876, 40.180323704708414, 20.327172849806264, -21.839611180731428, -48.62987163086912, 59.838938368451245, 13.395535768010992, 0.25231264286511035, -191.30593363002777], [-81.5551875132705, 22.282802106811385, -28.79762577209725, 23.64502294558038, -21.26684506735397, 4.74364565833921, 87.83405607682545, -33.94788859085822, -70.30804229060762], [14.686165831386798, -38.71489312433175, 50.39107551359443, -51.193449699327694, -21.198139474934802, 113.03039186391185, 1.0281229149147642, -55.325855536257016, -35.8978278149893], [-59.93937323367917, -18.14112190533648, 68.92039541180003, -1.681750006382603, -25.417579302837204, 43.5621133089547, -21.45819113203375, 19.564613063962902, -63.175090255352664], [-35.48409168968366, 16.2081226396706, -55.878738136582356, 99.84691108180476, -50.58471438463333, 68.71471597683893, -9.751909892350884, 109.19357115768067, -1.1110218775723766], [-60.87090311148353, 30.403343224366353, 22.56323409207796, 6.493263291316902, -34.98912352551494, -7.442844029015325, -22.621593539038024, -93.43901259154077, -54.38277615320678], [-36.25400769625131, -29.228147476760327, -36.363796443445125, -5.7614860748672, -27.491925931884463, -53.98663750952032, -138.1284124736687, 53.598257858465146, -101.42005275539499], [6.563224227366623, 46.70029989441332, 111.49103359166823, -46.38925474609857, -3.164889909715079, 20.00652450681111, -17.18977307728226, 64.49186201593274, 158.77383091744665], [39.691154805003876, 62.00280318740535, 40.75230001875233, 1.6283082114489131, -0.2864126140724341, -124.41528478023326, 53.55682847983755, 2.323084296527716, 6.985664143351815], [-100.97195167313959, -28.88120508283535, -4.537320480566146, 25.218945670067306, -35.32555005905596, 72.32874046193903, 83.82199946450164, -11.789937414481109, 7.869130955524228], [-27.136028517368214, 36.555032705414874, 23.443207817550093, 18.497908993038223, -4.547672210507583, 172.28012727256956, 74.66415579107814, 1.8055405169421936, -55.22493186904762], [-14.535529838231337, 13.017681535476562, 63.13444017245396, 71.4374550874391, 24.449234875754968, -82.87686968514917, 25.303842115532248, 9.106699954863211, -22.199042618225285], [30.526361325300684, -27.023390298192005, -43.82595212110778, 4.401738631280368, -10.104803226622483, -58.14590533640092, 30.649412951386942, -16.771918317204737, 52.838957030664645], [-47.639711783566405, -39.07602894900697, -14.554190522447783, -75.12214394952134, 107.68623141975294, 56.69195094988675, -7.798518590617233, -4.7813546925045, -50.60551328677547], [-12.538247036897717, 48.45696131467756, 75.02398511938902, 75.53094643505176, -8.888208501939541, -42.18055358673861, 3.3887997725660517, -0.1489183565137573, -21.777817172783333], [2.4964783558620756, 2.204724553004244, 13.90263448985387, -31.071644825568896, -62.05891806007307, -20.695199226781394, -21.452710814850406, -107.2726510860868, -49.8289256860888]], [[-9.367246352526445], [12.800924325891996], [-7.071897268849225], [-38.81469422578317], [-36.077167561667196], [-9.143848166089835], [0.9168968525389172], [-45.33342670845391], [-47.49278694710627]], [[]]]}}
    neural = neural['net']
    new_net = Network()
    bot = new_net._import(neural)
    game = Game(board)
    game.move(game.board, move)
    bots_move = bot.get_move(game)
    return new_board(game.board, bots_move, 'O')


if __name__ == "__main__":  # pragma: no cover
    """."""
    test = Generation([])
    test = test.new_random(10)
    for i in test.individuals:
        while i.age != 8:
            test.run()
            test = test.next_under_greedybot(.05)
        with open('testpickle', 'wb') as fp:
            pickle.dump(test.export(), fp)
        with open('testpickle', 'rb') as fp:
            imported = test.gen_import(pickle.load(fp))
        break
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
        # board_list = []
        # for x in game.board:
        #     board_list.append(x)
        # game.move(game.board, b(board_list, game.turn))
        game.move(game.board, b.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            break
    game = Game()
    a = test.individuals[0]
    b = test.individuals[1]
    # a = test.individuals[0]
    # b = greedy_bot
    while True:
        # board_list = []
        # for x in game.board:
        #     board_list.append(x)
        # game.move(game.board, b(board_list, game.turn))
        game.move(game.board, b.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            break
        if ' ' not in game.board:
            break
        game.move(game.board, a.net.get_move(game))
        print('------')
        print('|', game.board[0:3], '|')
        print('|', game.board[3:6], '|')
        print('|', game.board[6:9], '|')
        print('------')
        if game.winner is not None:
            break
        if ' ' not in game.board:
            break
    buckets = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
    }
    for i in test.individuals:
        game = Game()
        buckets[i.net.get_move(game)] += 1
    print(buckets)
    print('why we be here?')

