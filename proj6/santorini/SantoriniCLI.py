"""
SantoriniCLI module
-------------------
Implements the bare-bones CLI required to run the Santorini game
based on the command line arguments passed from the front-end
"""

from .state import (SantoriniStateBase, SantoriniStateInitial)
from .memento import SantoriniCaretaker, SantoriniOriginator


class SantoriniCLI():
    """
    SantoriniCLI
    ------------
    Basic CLI interface that maintains the context for the game's states,
    including the Memento-related objects to maintain history, and maintains
    the main loop of the game
    """

    _state: SantoriniStateBase = None

    def __init__(self, **kwargs) -> None:
        self._args = kwargs
        self.players = None
        self.caretaker: SantoriniCaretaker = None
        self.originator: SantoriniOriginator = None
        self.transition_to(SantoriniStateInitial())

    def _get_args(self) -> dict:
        return self._args

    args = property(_get_args)

    def transition_to(self, state) -> None:
        """Changes the context's state to the given state"""
        self._state = state
        self._state.context = self

    def run(self) -> None:
        """Runs the main loop of the game"""
        while True:
            self._state.run()
