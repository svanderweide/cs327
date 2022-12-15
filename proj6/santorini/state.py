"""
SantoriniState module
---------------------
Implements the various states required for a Santorini game
and allows extensions to new interfaces with minimal changes
"""

import sys
from abc import ABC, abstractmethod

from .board import SantoriniBoard
from .worker import SantoriniWorker
from .player import (SantoriniPlayerHuman, SantoriniPlayerRandom, SantoriniPlayerHeuristic)

from .decorators import log_heuristic_score

class SantoriniStateBase(ABC):
    """
    SantoriniStateBase
    ------------------
    Abstract state class with abstract method for performing the state
    """
    def __init__(self) -> None:
        super().__init__()
        self._context = None

    def _get_context(self):
        return self._context

    def _set_context(self, context):
        self._context = context

    context = property(_get_context, _set_context)

    @abstractmethod
    def run(self) -> bool:
        pass


class SantoriniStateInitial(SantoriniStateBase):
    """
    SantoriniStateInitial
    ---------------------
    Concrete state class used to set up and prepare to run the game
    """

    def _create_players(self, args):

        players = []

        # hard-coded for 2-player CLI version
        templates = [ 
            { 'col': 'white', 'template': args.get('white'), 'names': ['A', 'B'] },
            { 'col': 'blue',  'template': args.get('blue'),  'names': ['Y', 'Z'] },
        ]

        # not fully hard-coded but depends on the values
        # defined above in the hard-coded portion
        for template in templates:
            if template['template'] == 'human':
                player = SantoriniPlayerHuman(template['col'], template['names'])
            elif template['template'] == 'random':
                player = SantoriniPlayerRandom(template['col'], template['names'])
            elif template['template'] == 'heuristic':
                player = SantoriniPlayerHeuristic(template['col'], template['names'])
            players.append(player)

        if args.get('score') == 'on':
            board = self.context.board
            for player in players:
                player.get_description = log_heuristic_score(player.get_description, player, board)

        return players

    def _create_workers(self) -> list[SantoriniWorker]:

        # hard-coded for 2-player CLI version
        workers = [
            SantoriniWorker('white', 'A', (3, 1)),
            SantoriniWorker('white', 'B', (1, 3)),
            SantoriniWorker('blue', 'Y', (1, 1)),
            SantoriniWorker('blue', 'Z', (3, 3)),
        ]

        return workers

    def run(self) -> None:

        # create board and players
        self.context.board = SantoriniBoard(workers=self._create_workers())
        self.context.players = self._create_players(self._context.args)

        # transition to next state
        self.context.transition_to(SantoriniStateRunning(0))


class SantoriniStateRunning(SantoriniStateBase):
    """
    SantoriniStateRunning
    ---------------------
    Concrete state class used to set up and prepare to run the game
    """

    def __init__(self, turn: int) -> None:
        super().__init__()
        self._turn = turn
        self._player = None

    def _get_context(self):
        return super()._get_context()

    def _set_context(self, context):
        super()._set_context(context)
        self._player = self.context.players[self._turn % len(self.context.players)]

    # subclass the 'context' setter to update 'player' attribute
    context = property(_get_context, _set_context)

    def run(self) -> None:

        # print the current turn information
        print(self.context.board)
        print(f'Turn: {self._turn + 1}, ', end='')
        print(self._player.get_description(self.context.board))

        # check for termination
        if self.context.board.check_termination(self._player):
            self.context.transition_to(SantoriniStateEnd(self._turn + 1))
            return

        # player takes their turn
        self._player.take_turn(self._context.board)

        # go to next turn
        self.context.transition_to(SantoriniStateRunning(self._turn + 1))


class SantoriniStateEnd(SantoriniStateBase):

    def __init__(self, turn: int) -> None:
        super().__init__()
        self._turn = turn
        self._player = None

    def _get_context(self):
        return super()._get_context()

    def _set_context(self, context):
        super()._set_context(context)
        self._player = self.context.players[self._turn % len(self.context.players)]

    # subclass the 'context' setter to update 'player' attribute
    context = property(_get_context, _set_context)

    def run(self) -> None:

        print(f'{self._player.col} has won')
        sys.exit(0)
