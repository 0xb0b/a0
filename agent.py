
def interact(policy, game, model=None):
    action = policy.get_action(game, model)
    if action is not None:
        observed_state = game.accept(action)
        if model is not None:
            model.update(observed_state)
