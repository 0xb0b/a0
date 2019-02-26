import pytest
from game import Game


def rotate(state, size, num_rotations=1):
    # rotate input state (immutable) counter clockwise given number of times
    # and return as a new mutable state
    result_state = list(state)
    if num_rotations == 0:
        return result_state
    temp_state = list(state)
    for _ in range(num_rotations):
        for i, tile in enumerate(temp_state):
            result_state[size * (size - 1 - i % size) + i // size] = tile
        temp_state = result_state[:]
    return result_state


@pytest.mark.parametrize("input_state, rotated_state, size", [
                          ((3,),
                           [3], 1),
                          ((1, 2, 3, 4),
                           [2, 4, 1, 3], 2),
                          ((1, 2, 3, 4, 5, 6, 7, 8, 9),
                           [3, 6, 9, 2, 5, 8, 1, 4, 7], 3),
                          ((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5),
                           [3, 7, 1, 5, 2, 6, 0, 4, 1, 5, 9, 3, 0, 4, 8, 2], 4)
                          ])
def test_rotate(input_state, rotated_state, size):
    assert rotate(input_state, size) == rotated_state


@pytest.fixture
def game_instance():
    return Game()


interact_state_examples = [
    # (initial state, final state)
    # each example pair is defined for action.RIGHT, all other actions with
    # correspondingly rotated states have to be tested in addition

    # empty state does not change
    ((0,) * 16, (0,) * 16),

    # non empty state does not change
    # 0 1 2 3     0 1 2 3
    # 0 0 0 4 --> 0 0 0 4
    # 5 2 1 6     5 2 1 6
    # 0 0 0 0     0 0 0 0
    ((0, 1, 2, 3, 0, 0, 0, 4, 5, 2, 1, 6, 0, 0, 0, 0),
     (0, 1, 2, 3, 0, 0, 0, 4, 5, 2, 1, 6, 0, 0, 0, 0)),

    # terminal state does not change
    # 3 1 2 3     3 1 2 3
    # 1 2 8 4 --> 1 2 8 4
    # 5 3 1 6     5 3 1 6
    # 1 2 3 5     1 2 3 5
    ((3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5),
     (3, 1, 2, 3, 1, 2, 8, 4, 5, 3, 1, 6, 1, 2, 3, 5)),

    # tiles moved, no merging
    # 0 1 2 0     0 0 1 2
    # 0 4 0 0 --> 0 0 0 4
    # 5 2 1 0     0 5 2 1
    # 6 0 3 0     0 0 6 3
    ((0, 1, 2, 0, 0, 4, 0, 0, 5, 2, 1, 0, 6, 0, 3, 0),
     (0, 0, 1, 2, 0, 0, 0, 4, 0, 5, 2, 1, 0, 0, 6, 3)),

    # tiles moved and merged
    # 0 1 2 2     0 0 1 3
    # 0 4 0 4 --> 0 0 0 5
    # 2 2 1 0     0 0 3 1
    # 3 0 3 7     0 0 4 7
    ((0, 1, 2, 2, 0, 4, 0, 4, 2, 2, 1, 0, 3, 0, 3, 7),
     (0, 0, 1, 3, 0, 0, 0, 5, 0, 0, 3, 1, 0, 0, 4, 7)),

    # double merges
    # 1 1 2 2     0 0 2 3
    # 0 5 4 4 --> 0 0 5 5
    # 2 0 2 3     0 0 3 3
    # 3 3 3 3     0 0 4 4
    ((1, 1, 2, 2, 0, 5, 4, 4, 2, 0, 2, 3, 3, 3, 3, 3),
     (0, 0, 2, 3, 0, 0, 5, 5, 0, 0, 3, 3, 0, 0, 4, 4)),
]


@pytest.mark.parametrize("initial_state, final_state", interact_state_examples)
def test_game_interact(game_instance, initial_state, final_state):
    # copy example data to local mutable variables
    num_rotations = 0
    for action in game_instance.actions():
        state = rotate(initial_state, game_instance.size, num_rotations)
        expected_state = rotate(final_state, game_instance.size, num_rotations)
        game_instance.interact(action, state)
        assert state == expected_state
        num_rotations += 1


possible_actions_state_examples = [
    # (state, possible actions)
    # actions are enumerated as integers: RIGHT: 0, UP: 1, LEFT: 2, DOWN: 3

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
    assert game_instance.get_possible_actions(state) == [
        game_instance.action[name] for name in possible_actions]


def test_is_terminal(game_instance):
    assert not game_instance.is_terminal([0, 1, 2, 0,
                                          0, 4, 0, 0,
                                          5, 2, 1, 0,
                                          6, 0, 3, 0])
    assert game_instance.is_terminal([3, 1, 2, 3,
                                      1, 2, 8, 4,
                                      5, 3, 1, 6,
                                      1, 2, 3, 5])


def test_generate_tile(game_instance):
    num_tiles = 16
    state = [0] * num_tiles
    for _ in range(num_tiles):
        game_instance.generate_tile(state)
    for tile in state:
        assert tile == 1 or tile == 2
    old_state = state[:]
    game_instance.generate_tile(state)
    assert state == old_state


update_score_state_examples = [
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
    ([0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 2),

    # tiles moved and merged
    # 0 1 2 2     0 0 1 3
    # 0 4 0 4 --> 0 0 0 5
    # 2 2 1 0     0 0 3 1
    # 3 0 3 7     0 0 4 7
    ([0, 1, 2, 2, 0, 4, 0, 4, 2, 2, 1, 0, 3, 0, 3, 7], 5 + 4 + 3 + 3),

    # double merges
    # 1 1 2 2     0 0 2 3
    # 0 5 4 4 --> 0 0 5 5
    # 2 0 2 3     0 0 3 3
    # 3 3 3 3     0 0 4 4
    ([1, 1, 2, 2, 0, 5, 4, 4, 2, 0, 2, 3, 3, 3, 3, 3], 5 + 4 + 4 + 3 + 3 + 2),
]


@pytest.mark.parametrize("state, score", update_score_state_examples)
def test_score(game_instance, state, score):
    game_instance.state = state
    game_instance.move(game_instance.action.RIGHT)
    assert game_instance.score == score
