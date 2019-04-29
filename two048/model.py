
class Model:

    def __init__(self, trajectory=None):
        self.trajectory = [] if trajectory is None else trajectory[:]

    def update(self, observed_state):
        self.trajectory.append(observed_state)
