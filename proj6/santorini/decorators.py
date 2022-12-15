"""
decorators module for the Santorini game
"""

from functools import wraps
from .board import SantoriniBoard
from .player import SantoriniPlayerBase

def log_heuristic_score(fn, player: SantoriniPlayerBase, board: SantoriniBoard):

    def decorate(fn):

        @wraps(fn)

        def wrapped(*args, **kwargs):

            description = fn(*args, **kwargs)
            description += f', {board.get_heuristic_score(player)}'
            return description

        return wrapped

    return decorate(fn)
