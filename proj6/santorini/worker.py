"""Santorini worker module"""

class SantoriniWorker:

    def __init__(self, col: str, name: str) -> None:
        self._col = col
        self._name = name
        self._location = tuple()
    
    def _get_location(self) -> tuple:
        return self._location
    
    def _set_location(self, location: tuple) -> None:
        self._location = location
    
    location = property(_get_location, _set_location)

    def __str__(self) -> str:
        return f'{self._name}'
