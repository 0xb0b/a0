import random
from enum import Enum


def increment(tile):
    return tile + 1


class Game:

    # action space:
    #   actions enumerated starting from RIGHT and rotating counter clockwise
    action = Enum("action", "RIGHT, UP, LEFT, DOWN")

    empty_tile = 0

    def __init__(self, rseed=42, size=4, four_probability=0.1):
        random.seed(rseed)
        self.size = size
        self.four_p = four_probability
        self.state = [self.empty_tile] * size * size
        # make initial state nonempty so game state can never be empty
        self.generate_tile(self.state)
        self.history = []
        self.indices = {}
        rows = [tuple([i * size + j for j in range(size)])
                for i in range(size)]
        columns = [tuple([i + j * size for j in range(size)])
                   for i in range(size)]
        self.indices[self.action.UP] = tuple(columns)
        self.indices[self.action.DOWN] = tuple(
            [tuple(reversed(col)) for col in columns])
        self.indices[self.action.LEFT] = tuple(rows)
        self.indices[self.action.RIGHT] = tuple(
            [tuple(reversed(row)) for row in rows])
        self.score = 0

    def actions(self):
        return iter(self.action)

    def move(self, action):
        self.interact(action, self.state)
        self.update_score()
        self.generate_tile(self.state)
        self.history.append(self.state)

    def interact(self, action, state):
        # change the state according to the action.
        # modifies state in place.
        # slide the tiles as far as they will go in a direction defined by
        # action.
        # tiles do not merge recursively, if a pair is merged in a move then the
        # resulting tile can not be merged further in the same move:
        # 4   0   2-> 2
        #   4-> 0   0   4
        #     0   0   4   4
        for sequence_indices in self.indices[action]:
            stop_i = 0
            stop_index = sequence_indices[stop_i]
            for index in sequence_indices[1:]:
                if self.empty(index, state):
                    continue
                tile = state[index]
                self.clear_tile(index, state)
                if self.empty(stop_index, state):
                    state[stop_index] = tile
                elif state[stop_index] == tile:
                    state[stop_index] = increment(tile)
                    stop_i += 1
                    stop_index = sequence_indices[stop_i]
                else:
                    stop_i += 1
                    stop_index = sequence_indices[stop_i]
                    state[stop_index] = tile

    def empty(self, index, state):
        return state[index] == self.empty_tile

    def clear_tile(self, index, state):
        state[index] = self.empty_tile

    def update_score(self):
        min_tile = increment(self.empty_tile)
        prev_tiles = [tile for tile in self.history[-1] if tile > min_tile]
        current_tiles = [tile for tile in self.state if tile > min_tile]
        for tile in current_tiles:
            if tile in prev_tiles:
                prev_tiles.remove(tile)
            else:
                self.score += tile

    def generate_tile(self, state):
        # insert tile at random empty position
        # probabilities of the values of the new tile: {2: (1 - p), 4: p}
        tile = increment(self.empty_tile)
        if random.random() > self.four_p:
            tile = increment(tile)
        empty_index = random.choice([i for i in range(len(state))
                                     if self.empty(i, state)])
        state[empty_index] = tile

    def observe(self):
        # return information about the state
        # this can be the state itself or some partial information
        return self.state

    def evaluate(self):
        # return the value of the state (e.g. game score)
        return self.score

    def is_state_changed(self, action, state):
        for sequence_indices in self.indices[action]:
            stop_i = 0
            stop_index = sequence_indices[stop_i]
            for index in sequence_indices[1:]:
                if self.empty(index, state):
                    continue
                tile = state[index]
                if (self.empty(stop_index, state) or
                        state[stop_index] == tile or
                        sequence_indices[stop_i + 1] != index):
                    return True
                else:
                    stop_i += 1
                    stop_index = sequence_indices[stop_i]
        return False

    def get_possible_actions(self, state):
        return [action for action in self.action
                if self.is_state_changed(action, state)]

    def is_terminal(self, state):
        # if any further interaction is possible (e.g. is the game finished?)
        # state must be nonempty
        for action in self.action:
            if self.is_state_changed(action, state):
                return False
        else:
            return True
