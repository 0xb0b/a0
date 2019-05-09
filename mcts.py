class Tree:

    def __init__(self, parent=None):
        self.parent = parent
        self.statistics = None
        self.children = None
        self.visited_children = None


def expand(tree, game):
    # traverse the tree down from the root, select not fully expanded node and
    # expand - return new previously unvisited leaf
    # TODO what if the selected node is terminal and can not be expanded?
    pass


def evaluate(tree):
    # perform playout simulation or in some other way evaluate the tree node
    # returns statistics
    pass


def backpropagate(tree):
    statistics = tree.statistics
    tree = tree.parent
    while tree is not None:
        tree.update(statistics)
        tree = tree.parent


