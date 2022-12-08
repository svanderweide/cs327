
class SantoriniArchitect:

    def __init__(self, col: str, name: str, location: tuple) -> None:
        self._col = col
        self._name = name
        self._location = location

    def has_col(self, col: str) -> bool:
        return self._col == col

    def has_name(self, name: str) -> bool:
        return self._name == name

    def _get_location(self) -> tuple:
        return self._location
    
    def _set_location(self, location: tuple):
        self._location = location

    location = property(_get_location, _set_location)

    def __str__(self) -> str:
        return f'{self._name}'
