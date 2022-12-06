"""Santorini game board tile module"""

from santorini.structure import SantoriniStructure

class SantoriniBoardTile:
    """Santorini game board tile class"""

    def __init__(self, structure=None, worker=None) -> None:
        self._structure = structure if structure else SantoriniStructure()
        self._worker = worker

    def __str__(self) -> str:
        tile = f'{self._structure}'
        tile += f'{self._worker}' if self._worker else ' '
        return tile
