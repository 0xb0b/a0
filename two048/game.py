import random
from enum import Enum


class Game:
    # state, action space and the rules of the game

    # action space:
    #   actions enumerated starting from RIGHT and rotating counter clockwise
    ActionSpace = Enum("ActionSpace", "RIGHT, UP, LEFT, DOWN")

    empty_tile = 0

    def __init__(self, size=4, probability_of_4=0.1, state=None,
                 scoring="2048"):
        self.size = size
        self.score = 0
        self.scoring = scoring
        if scoring == "threes":
            self.update_score = self.score_threes
        else:
            self.update_score = self.score_2048
        self.p4 = probability_of_4

        self.prev_state = None
        if state is None:
            self.state = [self.empty_tile] * size * size
            # make initial state nonempty so that game state can never be empty
            self.generate_tile()
        else:
            self.state = state

        # sequences of indices - rows or columns with indices ordered according
        # to a certain move
        # e. g. rows of indices from left to right for move to the left
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

    def clone(self):
        cloned_game = Game(size=self.size, probability_of_4=self.p4,
                           state=self.state, scoring=self.scoring)
        cloned_game.set_value(self.score)
        return cloned_game

    def actions(self):
        return iter(self.ActionSpace)

    def get_state(self):
        return self.state[:]

    def get_value(self):
        # return the value of the state (e.g. game score)
        return self.score

    def is_state_changed(self, action):
        for indices in self.index_sequences[action]:
            stop_i = 0
            stop_index = indices[stop_i]
            for index in indices[1:]:
                tile = self.state[index]
                if tile == self.empty_tile:
                    continue
                if (self.state[stop_index] == self.empty_tile or
                        self.state[stop_index] == tile or
                        indices[stop_i + 1] != index):
                    return True
                else:
                    stop_i += 1
                    stop_index = indices[stop_i]
        return False

    def get_possible_actions(self):
        return [action for action in self.ActionSpace
                if self.is_state_changed(action)]

    def is_finished(self):
        # if any further interaction is possible (e.g. is the game finished?)
        for action in self.ActionSpace:
            if self.is_state_changed(action):
                return False
        else:
            return True

    def set_state(self, state):
        self.prev_state = None
        self.state = state

    def set_value(self, value=0):
        self.score = value

    def change_state(self, action):
        # change the state by applying the action:
        #   slide the tiles as far as they will go in a direction defined by
        #   action.
        #   tiles do not merge recursively - if a pair is merged in a move then
        #   the resulting tile can not be merged further in the same move:
        #   4  0  2  2  ->  4  0  0  4  ->  0   0   4   4
        #
        self.prev_state = self.state[:]
        for indices in self.index_sequences[action]:
            stop_i = 0
            stop_index = indices[stop_i]
            for index in indices[1:]:
                tile = self.state[index]
                if tile == self.empty_tile:
                    continue
                self.state[index] = self.empty_tile
                if self.state[stop_index] == self.empty_tile:
                    self.state[stop_index] = tile
                elif self.state[stop_index] == tile:
                    self.state[stop_index] = increment(tile)
                    stop_i += 1
                    stop_index = indices[stop_i]
                else:
                    stop_i += 1
                    stop_index = indices[stop_i]
                    self.state[stop_index] = tile

    def score_2048(self):
        # the score increases every time the two tiles are combined by the value
        # of the new tile
        min_tile = increment(self.empty_tile)
        prev_tiles = [tile for tile in self.prev_state if tile > min_tile]
        prev_tiles.sort()
        tiles = [tile for tile in self.state if tile > min_tile]
        tiles.sort(reverse=True)
        delta = 0
        for tile in tiles:
            if prev_tiles and tile == prev_tiles[-1]:
                prev_tiles.pop()
            else:
                # this tile is from merging two lower level tiles
                # in previous state
                delta += 1 << tile
                if prev_tiles:
                    prev_tiles.pop()
                    prev_tiles.pop()
        self.score += delta

    def score_threes(self):
        # each nonempty tile has a rank n:
        #   tile value = 2^n
        # score of a state is the sum of the scores of tiles present on the
        # board:
        #   tile score = 3^(n - 1) - 1
        score = 0
        for tile in self.state:
            if tile == self.empty_tile:
                continue
            score += pow(3, tile - 1) - 1
        self.score = score

    def generate_tile(self):
        # insert tile at random empty position
        # probabilities of the values of the new tile: {2: (1 - p), 4: p}
        tile = increment(self.empty_tile)  # tile 2
        if random.random() > self.p4:
            tile = increment(tile)  # tile 4
        empty_indices = [i for i in range(len(self.state))
                         if self.state[i] == self.empty_tile]
        if empty_indices:
            self.state[random.choice(empty_indices)] = tile

    def accept(self, action):
        self.change_state(action)
        self.update_score()
        self.generate_tile()
        return self.state[:]


def init_randomness(rseed=42):
    random.seed(rseed)


def increment(tile):
    return tile + 1



