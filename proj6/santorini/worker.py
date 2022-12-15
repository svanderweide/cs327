"""
Worker module
-------------
Implements the Worker class (mostly a data class) that provides
an object for the players to control as move around the board
"""

class SantoriniWorker:
    """
    SantoriniWorker
    ---------------
    Worker on the Santorini game board that belongs to a certain
    player according to its color, is represented by its name, and
    exists on a single tile on the board
    """

    def __init__(self, col: str, name: str, location: tuple) -> None:
        self._col = col
        self._name = name
        self._location = location

    def _get_col(self) -> str:
        return self._col

    col = property(_get_col)

    def _get_name(self) -> str:
        return self._name

    name = property(_get_name)

    def _get_location(self) -> tuple:
        return self._location

    def _set_location(self, location: tuple) -> None:
        self._location = location

    location = property(_get_location, _set_location)

    def __str__(self) -> str:
        return f'{self._name}'
