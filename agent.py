
def interact(policy, game, model):
    action = policy.get_action(game, model)
    if action is not None:
        observed_state = game.accept(action)
        model.update(observed_state)
