import random


class Tree:

    def __init__(self, state, parent=None):
        # how to pass game here? attach separate game instance to each node?
        # or add methods to game that take state as input to make moves?
        self.state = state
        self.parent = parent
        self.statistics = None
        self.children = None
        self.children_iterator = None
        self.unvisited_child = None
        self.is_expanded = False
        self.is_terminal = False

    def generate_children(self, game):
        pass

    def get_unvisited_child(self):
        if self.is_terminal:
            return None
        else:
            if self.unvisited_child is None:
                self.generate_children()
            leaf = self.unvisited_child
            try:
                self.unvisited_child = self.children_iterator.__next__()
            except StopIteration:
                self.is_expanded = True
            return leaf


def expand(root, game):
    # traverse the tree down from the root until not fully expanded node found
    # and expand this node - return new unvisited leaf
    # TODO what if the selected node is terminal?
    node = root
    while not node.is_terminal and node.is_expanded:
        # select best child according to UCB1
        node = None
    leaf = node.get_unvisited_child()
    return leaf


def evaluate(leaf):
    # perform playout simulation or in some other way evaluate the unvisited
    # tree node
    # returns statistics
    pass


def backpropagate(node):
    statistics = node.statistics
    node = node.parent
    while node is not None:
        node.update(statistics)
        node = node.parent


