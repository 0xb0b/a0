import pytest
from game import Game, init_randomness


def rotate(state, size, num_rotations=1):
    # rotate the input state counter clockwise given number of times and return
    # the rotated state
    if num_rotations == 0:
        return state
    for _ in range(num_rotations):
        temp_state = state[:]
        for i, tile in enumerate(temp_state):
            state[size * (size - 1 - i % size) + i // size] = tile
    return state


@pytest.mark.parametrize("input_state, rotated_state, size", [
                          ([3],
                           [3], 1),
                          ([1, 2, 3, 4],
                           [2, 4, 1, 3], 2),
                          ([1, 2, 3, 4, 5, 6, 7, 8, 9],
                           [3, 6, 9, 2, 5, 8, 1, 4, 7], 3),
                          ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5],
                           [3, 7, 1, 5, 2, 6, 0, 4, 1, 5, 9, 3, 0, 4, 8, 2], 4)
                          ])
def test_rotate(input_state, rotated_state, size):
    assert rotate(input_state, size) == rotated_state


@pytest.fixture
def game_instance():
    init_randomness()
    return Game()


interact_state_examples = [
    # (initial state, final state)
    # each example pair is defined for ActionSpace.RIGHT, all other actions with
    # correspondingly rotated states have to be tested in addition

    # empty state does not change
    ([0] * 16, [0] * 16),

    # non empty state does not change
    # 0 1 2 3     0 1 2 3
    # 0 0 0 4 --> 0 0 0 4
    # 5 2 1 6     5 2 1 6
    # 0 0 0 0     0 0 0 0
    ([0, 1, 2, 3, 0, 0, 0, 4, 5, 2, 1, 6, 0, 0, 0, 0],
     [0, 1, 2, 3, 0, 0, 0, 4, 5, 2, 1, 6, 0, 0, 0, 0]),

    # terminal state does not change
    # 3 1 2 3     3 1 2 3
    # 1 2 8 4 --> 1 2 8 4
    # 5 3 1 6     5 3 1 6
    # 1 2 3 5     1 2 3 5
    ([3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5],
     [3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5]),

    # tiles moved, no merging
    # 0 1 2 0     0 0 1 2
    # 0 4 0 0 --> 0 0 0 4
    # 5 2 1 0     0 5 2 1
    # 6 0 3 0     0 0 6 3
    ([0, 1, 2, 0, 0, 4, 0, 0, 5, 2, 1, 0, 6, 0, 3, 0],
     [0, 0, 1, 2, 0, 0, 0, 4, 0, 5, 2, 1, 0, 0, 6, 3]),

    # tiles moved and merged
    # 0 1 2 2     0 0 1 3
    # 0 4 0 4 --> 0 0 0 5
    # 2 2 1 0     0 0 3 1
    # 3 0 3 7     0 0 4 7
    ([0, 1, 2, 2, 0, 4, 0, 4, 2, 2, 1, 0, 3, 0, 3, 7],
     [0, 0, 1, 3, 0, 0, 0, 5, 0, 0, 3, 1, 0, 0, 4, 7]),

    # double merges
    # 1 1 2 2     0 0 2 3
    # 0 5 4 4 --> 0 0 5 5
    # 2 0 2 3     0 0 3 3
    # 3 3 3 3     0 0 4 4
    ([1, 1, 2, 2, 0, 5, 4, 4, 2, 0, 2, 3, 3, 3, 3, 3],
     [0, 0, 2, 3, 0, 0, 5, 5, 0, 0, 3, 3, 0, 0, 4, 4]),
]


@pytest.mark.parametrize("initial_state, final_state", interact_state_examples)
def test_change_state(game_instance, initial_state, final_state):
    # test that state is changed according to the rules
    # initial and final state parameters are defined for ActionSpace.RIGHT
    # all other actions are tested by rotating states
    # ActionSpace is expected to be ordered counter clockwise starting from
    # ActionSpace.RIGHT
    for action in game_instance.actions():
        game_instance.set_state(initial_state[:])
        game_instance.change_state(action)
        assert game_instance.get_state() == final_state
        rotate(initial_state, game_instance.size)
        rotate(final_state, game_instance.size)


possible_actions_state_examples = [
    # (state, possible actions)

    # empty state, no actions possible
    ([0] * 16, ()),

    # non empty state, all actions possible
    # 0 1 2 0
    # 0 4 0 0
    # 5 2 1 0
    # 6 0 3 0
    ([0, 1, 2, 0, 0, 4, 0, 0, 5, 2, 1, 0, 6, 0, 3, 0],
     ("RIGHT", "UP", "LEFT", "DOWN")),

    # all actions except RIGHT possible
    # 0 1 2 3
    # 0 0 0 4
    # 5 2 1 6
    # 0 0 0 0
    ([0, 1, 2, 3, 0, 0, 0, 4, 5, 2, 1, 6, 0, 0, 0, 0], ("UP", "LEFT", "DOWN")),

    # only actions LEFT and DOWN possible
    # 0 1 2 1
    # 0 3 1 4
    # 0 0 2 5
    # 0 0 0 0
    ([0, 1, 2, 1, 0, 3, 1, 4, 0, 0, 2, 5, 0, 0, 0, 0], ("LEFT", "DOWN")),

    # only actions LEFT and RIGHT possible
    # 0 1 0 3
    # 0 3 0 1
    # 0 2 0 2
    # 0 5 0 4
    ([0, 1, 0, 3, 0, 3, 0, 1, 0, 2, 0, 2, 0, 5, 0, 4], ("RIGHT", "LEFT")),

    # only action UP possible
    # 0 0 0 0
    # 0 0 0 0
    # 6 2 1 3
    # 3 1 2 7
    ([0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 1, 3, 3, 1, 2, 7], ("UP",)),

    # terminal state
    # 3 1 2 3
    # 1 2 8 4
    # 5 3 1 6
    # 1 2 3 5
    ([3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5], ())
]


@pytest.mark.parametrize("state, possible_actions",
                         possible_actions_state_examples)
def test_get_possible_actions(game_instance, state, possible_actions):
    game_instance.set_state(state)
    assert game_instance.get_possible_actions() == [
        game_instance.ActionSpace[name] for name in possible_actions]


def test_is_terminal(game_instance):
    game_instance.set_state([0, 1, 2, 0,
                             0, 4, 0, 0,
                             5, 2, 1, 0,
                             6, 0, 3, 0])
    assert not game_instance.is_finished()

    game_instance.set_state([3, 1, 2, 3,
                             1, 2, 8, 4,
                             5, 3, 1, 6,
                             1, 2, 3, 5])
    assert game_instance.is_finished()


def test_generate_tile(game_instance):
    num_empty_tiles = game_instance.size * game_instance.size - 1
    for _ in range(num_empty_tiles):
        game_instance.generate_tile()
    state = game_instance.get_state()
    for tile in state:
        assert tile == 1 or tile == 2
    game_instance.generate_tile()
    assert game_instance.get_state() == state


update_score_2048_state_examples = [
    # (state, score)

    # tiles do not move, score does not change
    # 0 1 2 3     0 1 2 3
    # 0 0 0 4 --> 0 0 0 4
    # 5 2 1 6     5 2 1 6
    # 0 0 0 0     0 0 0 0
    ([0, 1, 2, 3, 0, 0, 0, 4, 5, 2, 1, 6, 0, 0, 0, 0], 0),

    # terminal state, score does not change
    # 3 1 2 3     3 1 2 3
    # 1 2 8 4 --> 1 2 8 4
    # 5 3 1 6     5 3 1 6
    # 1 2 3 5     1 2 3 5
    ([3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5], 0),

    # tiles moved, no merging, score does not change
    # 0 1 2 0     0 0 1 2
    # 0 4 0 0 --> 0 0 0 4
    # 5 2 1 0     0 5 2 1
    # 6 0 3 0     0 0 6 3
    ([0, 1, 2, 0, 0, 4, 0, 0, 5, 2, 1, 0, 6, 0, 3, 0], 0),

    # tiles moved and merged
    # 0 0 0 0     0 0 0 0
    # 0 1 0 1 --> 0 0 0 2
    # 0 0 0 0     0 0 0 0
    # 0 0 0 0     0 0 0 0
    ([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 4),

    # tiles moved and merged
    # 0 1 2 2     0 0 1 3
    # 0 4 0 4 --> 0 0 0 5
    # 2 2 1 0     0 0 3 1
    # 3 0 3 7     0 0 4 7
    ([0, 1, 2, 2, 0, 4, 0, 4, 2, 2, 1, 0, 3, 0, 3, 7], 32 + 16 + 8 + 8),

    # double merges
    # 1 1 2 2     0 0 2 3
    # 0 5 4 4 --> 0 0 5 5
    # 2 0 2 3     0 0 3 3
    # 3 3 3 3     0 0 4 4
    ([1, 1, 2, 2, 0, 5, 4, 4, 2, 0, 2, 3, 3, 3, 3, 3], 32 + 16 + 16 + 8 + 8 + 4),
]


@pytest.mark.parametrize("state, score", update_score_2048_state_examples)
def test_score_2048(game_instance, state, score):
    game_instance.set_state(state)
    game_instance.set_value()
    game_instance.accept(game_instance.ActionSpace.RIGHT)
    assert game_instance.get_value() == score


update_score_threes_state_examples = [
    # (state, score)

    # state with only minimal tiles
    # 0 1 0 0
    # 0 0 0 0
    # 0 0 1 0
    # 0 0 0 0
    ([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], 0),

    # non terminal state
    # 0 1 2 0
    # 0 4 0 0
    # 5 2 1 0
    # 6 0 3 0
    ([0, 1, 2, 0, 0, 4, 0, 0, 5, 2, 1, 0, 6, 0, 3, 0], 2 + 26 + 80 + 2 + 242 + 8),

    # terminal state
    # 3 1 2 3
    # 1 2 8 4
    # 5 3 1 6
    # 1 2 3 5
    ([3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5], 8 + 2 + 8 + 2 + 2186 + 26 + 80 + 8 + 242 + 2 + 8 + 80),
]


@pytest.mark.parametrize("state, score", update_score_threes_state_examples)
def test_score_threes(state, score):
    game_instance = Game(state=state, scoring="threes")
    game_instance.update_score()
    assert game_instance.get_value() == score

