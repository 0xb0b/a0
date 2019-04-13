import random
from enum import Enum


def increment(tile):
    return tile + 1


class Game:

    # action space:
    #   actions enumerated starting from RIGHT and rotating counter clockwise
    ActionSpace = Enum("ActionSpace", "RIGHT, UP, LEFT, DOWN")

    empty_tile = 0

    def __init__(self, rseed=42, size=4, probability_of_4=0.1):
        random.seed(rseed)
        self.size = size
        self.score = 0
        self.p4 = probability_of_4

        self.prev_state = []
        self.state = [self.empty_tile] * size * size
        # make initial state nonempty so that game state can never be empty
        self.generate_tile(self.state)

        # sequences of indices corresponding to different moves
        self.index_sequences = {}
        rows = [tuple([i * size + j for j in range(size)])
                for i in range(size)]
        columns = [tuple([i + j * size for j in range(size)])
                   for i in range(size)]
        self.index_sequences[self.ActionSpace.UP] = tuple(columns)
        self.index_sequences[self.ActionSpace.DOWN] = tuple(
            [tuple(reversed(col)) for col in columns])
        self.index_sequences[self.ActionSpace.LEFT] = tuple(rows)
        self.index_sequences[self.ActionSpace.RIGHT] = tuple(
            [tuple(reversed(row)) for row in rows])

    def actions(self):
        return iter(self.ActionSpace)

    def accept(self, action):
        # save current state and change it
        self.prev_state = self.state[:]
        self.change(action, self.state)
        self.update_score()
        return self.state[:]

    def change(self, action, state):
        # change the state according to the action:
        #   slide the tiles as far as they will go in a direction defined by
        #   action.
        #   tiles do not merge recursively, if a pair is merged in a move then
        #   the resulting tile can not be merged further in the same move:
        #   4  0  2  2  ->  4  0  0  4  ->  0   0   4   4
        #
        # modifies state in place.
        for indices in self.index_sequences[action]:
            stop_i = 0
            stop_index = indices[stop_i]
            for index in indices[1:]:
                if self.is_tile_empty(index, state):
                    continue
                tile = state[index]
                self.clear_tile(index, state)
                if self.is_tile_empty(stop_index, state):
                    state[stop_index] = tile
                elif state[stop_index] == tile:
                    state[stop_index] = increment(tile)
                    stop_i += 1
                    stop_index = indices[stop_i]
                else:
                    stop_i += 1
                    stop_index = indices[stop_i]
                    state[stop_index] = tile

    def is_tile_empty(self, index, state):
        return state[index] == self.empty_tile

    def clear_tile(self, index, state):
        state[index] = self.empty_tile

    def update_score(self):
        self.score += self.diff_score(self.state, self.prev_state)

    def diff_score(self, state, prev_state):
        # TODO describe what the score is and how it is calculated
        min_tile = increment(self.empty_tile)
        prev_tiles = [tile for tile in prev_state if tile > min_tile]
        prev_tiles.sort()
        tiles = [tile for tile in state if tile > min_tile]
        tiles.sort(reverse=True)
        score = 0
        for tile in tiles:
            if prev_tiles and tile == prev_tiles[-1]:
                prev_tiles.pop()
            else:
                # this tile is from merging two lower level tiles
                # in previous state
                score += tile
                if prev_tiles:
                    prev_tiles.pop()
                    prev_tiles.pop()
        return score

    def generate_tile(self, state):
        # insert tile at random empty position
        # probabilities of the values of the new tile: {2: (1 - p), 4: p}
        tile = increment(self.empty_tile)  # tile 2
        if random.random() > self.p4:
            tile = increment(tile)  # tile 4
        empty_indices = [i for i in range(len(state))
                         if self.is_tile_empty(i, state)]
        if empty_indices:
            state[random.choice(empty_indices)] = tile

    def get_state(self):
        return self.state[:]

    def get_value(self):
        # return the value of the state (e.g. game score)
        return self.score

    def is_state_changed(self, action, state):
        for indices in self.index_sequences[action]:
            stop_i = 0
            stop_index = indices[stop_i]
            for index in indices[1:]:
                if self.is_tile_empty(index, state):
                    continue
                tile = state[index]
                if (self.is_tile_empty(stop_index, state) or
                        state[stop_index] == tile or
                        indices[stop_i + 1] != index):
                    return True
                else:
                    stop_i += 1
                    stop_index = indices[stop_i]
        return False

    def get_possible_actions(self, state):
        return [action for action in self.ActionSpace
                if self.is_state_changed(action, state)]

    def is_terminal(self, state):
        # if any further interaction is possible (e.g. is the game finished?)
        # state must be nonempty
        for action in self.ActionSpace:
            if self.is_state_changed(action, state):
                return False
        else:
            return True

