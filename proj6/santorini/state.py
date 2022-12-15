"""
State module
------------
Implements the various states required for a Santorini game
and allows extensions to new interfaces with minimal changes
"""

import sys
from abc import ABC, abstractmethod

from .board import SantoriniBoard
from .worker import SantoriniWorker
from .player import (SantoriniPlayerHuman, SantoriniPlayerRandom, SantoriniPlayerHeuristic)

from .decorators import add_heuristic_score
from .memento import SantoriniOriginator, SantoriniCaretaker

class SantoriniStateBase(ABC):
    """
    SantoriniStateBase
    ------------------
    Abstract state class with abstract method for performing the state's actions
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
        """Perform the action defined for the given state"""
        pass


class SantoriniStateInitial(SantoriniStateBase):
    """
    SantoriniStateInitial
    ---------------------
    Concrete state class responsible for setting up the game
    """

    def _create_players(self):

        players = []

        args = self.context.args

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

        # create board
        board = SantoriniBoard(workers=self._create_workers())

        # create players
        self.context.players = self._create_players()

        # create originator and caretaker for mementos
        self.context.originator = SantoriniOriginator(None)
        self.context.caretaker = SantoriniCaretaker(self.context.originator)

        # transition to running state
        self.context.originator.state = 0, board
        self.context.transition_to(SantoriniStateRunning())


class SantoriniStateRunning(SantoriniStateBase):
    """
    SantoriniStateRunning
    ---------------------
    Concrete state class responsible for maintaining the ordinary loop of the game
    and checking for the end conditions to be met for transition to next state
    """

    def __init__(self) -> None:
        super().__init__()
        self._turn = None
        self._board = None

    def run(self) -> None:

        self._turn, self._board = self.context.originator.state

        if self.context.args.get('score') == 'on':
            for player in self.context.players:
                # decorate the get_description method to show the heuristic score
                decorated = add_heuristic_score(player.base_get_description, player, self._board)
                player.get_description = decorated

        player = self.context.players[self._turn % len(self.context.players)]

        # print the current turn information
        print(self._board)
        print(f'Turn: {self._turn + 1}, ', end='')
        print(player.get_description(self._board))

        # check for termination
        if self._board.check_termination(player):
            self.context.transition_to(SantoriniStateEnd(self._turn + 1))
            return

        # check for undo/redo/next (if enabled)
        if self.context.args.get('history') == 'on':
            while True:
                print('undo, redo, or next')
                option = input()
                if option == 'undo':
                    self.context.caretaker.undo()
                    return
                if option == 'redo':
                    self.context.caretaker.redo()
                    return
                if option == 'next':
                    self.context.caretaker.next()
                    break
                print('Invalid. Accepted options: (undo/redo/next)')

        # save the state of the game before the turn
        self.context.caretaker.save()

        # player takes their turn
        player.take_turn(self._board)

        # go to next turn
        self.context.originator.state = self._turn + 1, self._board


class SantoriniStateEnd(SantoriniStateBase):
    """
    SantoriniStateEnd
    -----------------
    Concrete state class responsible for printing the victory message
    and ending the game by exiting the program
    """

    def __init__(self, turn: int) -> None:
        super().__init__()
        self._turn = turn

    def run(self) -> None:

        player = self.context.players[self._turn % len(self.context.players)]
        print(f'{player.col} has won')
        sys.exit(0)
