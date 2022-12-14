"""
Santorini game driver module

Responsible for setting up, launching, and monitoring
the state of the game for termination conditions
"""

from santorini.state import (SantoriniStateBase, SantoriniStateInitial)

class SantoriniCLI():

    _state: SantoriniStateBase = None

    def __init__(self, **kwargs) -> None:
        self._args = kwargs
        self.board = None
        self.players = None
        self.transition_to(SantoriniStateInitial())

    def _get_args(self) -> dict:
        return self._args
    
    args = property(_get_args)

    def transition_to(self, state) -> None:
        self._state = state
        self._state.context = self

    def run(self) -> None:
        while True:
            self._state.run()
