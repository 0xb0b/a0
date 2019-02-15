
UP, DOWN, LEFT, RIGHT = range(4)


class Game:

    action_space = (UP, DOWN, LEFT, RIGHT)
    empty_cell = 0

    def __init__(self, size=4):
        self.size = size
        self.state = [self.empty_cell] * size * size
        self.history = []
        self.indices = {}
        rows = [tuple([i * size + j for j in range(size)])
                for i in range(size)]
        columns = [tuple([i + j * size for j in range(size)])
                   for i in range(size)]
        self.indices[UP] = tuple(columns)
        self.indices[DOWN] = tuple([tuple(reversed(col)) for col in columns])
        self.indices[LEFT] = tuple(rows)
        self.indices[RIGHT] = tuple([tuple(reversed(row)) for row in rows])

    def interact(self, action):
        # change the state according to the action
        for sequence_indices in self.indices[action]:
            stop_index = sequence_indices[0]
            for i in sequence_indices[1:]:
                cell = self.state[i]
                if cell == self.empty_cell:
                    continue
                self.state[i] = self.empty_cell
                if self.state[stop_index] == self.empty_cell:
                    self.state[stop_index] = cell
                elif self.state[stop_index] == cell:
                    self.state[stop_index] += 1
                else:
                    stop_index += 1
                    self.state[stop_index] = cell

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
