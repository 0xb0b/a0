import random


class RandomPolicy:
    def get_action(self, game, _):
        actions = game.get_possible_actions()
        return random.choice(actions) if actions else None
