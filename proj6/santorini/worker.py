"""Santorini worker module"""

class SantoriniWorker:

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
