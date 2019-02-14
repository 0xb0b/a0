
UP, DOWN, LEFT, RIGHT = range(4)


class Game:

    def __init__(self, size=4):
        self.size = size
        self.state = [0] * size * size
        self.history = []
        self.action_space = (UP, DOWN, LEFT, RIGHT)
        self.indices = {}
        # TODO replace with iterators?
        rows = [tuple([i * 4 + j for j in range(self.size)])
                for i in range(self.size)]
        self.indices[RIGHT] = tuple(rows)
        self.indices[LEFT] = tuple([tuple(reversed(row)) for row in rows])
        columns = [tuple([i + j * 4 for j in range(self.size)])
                   for i in range(self.size)]
        self.indices[DOWN] = tuple(columns)
        self.indices[UP] = tuple([tuple(reversed(col)) for col in columns])

    def interact(self, action):
        # change the state according to the action
        pass

    def observe(self):
        # return information about the state
        # this can be the state itself or some partial information
        return self.state

    def evaluate(self):
        # return the value of the state (e.g. game score)
        return 0

    def is_terminal_state(self):
        # is any further interaction possible (e.g. is the game finished?)
        return True
