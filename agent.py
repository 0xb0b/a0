from a0.policy import get_random_action


class RandomAgent:

    def __init__(self, game):
        self.game = game
        self.action_space = [action for action in game.actions()]

    def take_action(self):
        action = get_random_action(self.action_space)
        self.game.advance(action)
