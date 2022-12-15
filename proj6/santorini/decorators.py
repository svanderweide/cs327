"""
Decorators module
-----------------
Implements the decorators required for the Santorini game as described
with easy extension / expansion if more decorators are required
"""

from functools import wraps

def add_heuristic_score(func, player, board):
    """Add the log of the heuristic score to the player's description"""

    def decorate(func):

        @wraps(func)

        def wrapped(*args, **kwargs):

            description = func(*args, **kwargs)
            description += f', {board.get_heuristic_score(player)}'
            return description

        return wrapped

    return decorate(func)
