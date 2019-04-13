from model import Model
from policy import get_random_action


class RandomAgent:

    def __init__(self, game):
        self.action_space = [action for action in game.actions()]
        self.model = Model()

    def act(self, game):
        action = get_random_action(self.action_space)
        observed_state = game.accept(action)
        self.model.update(observed_state)
