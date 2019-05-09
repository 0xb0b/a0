import random
import agent


class Random:
    def get_action(self, game, _):
        actions = game.get_possible_actions()
        return random.choice(actions) if actions else None


class PureMCTS:
    def __init__(self, samples=100):
        self.samples = samples
        self.playout_policy = Random()

    def configure(self, samples=None):
        if samples is not None:
            self.samples = samples

    def get_action(self, game, _):
        actions = game.get_possible_actions()
        if not actions:
            return None
        max_value = 0
        best_actions = []
        for action in actions:
            value = 0
            for _ in range(self.samples):
                playout_game = game.clone()
                playout_game.accept(action)
                while not playout_game.is_finished():
                    agent.interact(self.playout_policy, playout_game)
                value += playout_game.get_value()
            value /= self.samples
            if value == max_value:
                best_actions.append(action)
            elif value > max_value:
                best_actions = [action]
                max_value = value
        return random.choice(best_actions)




