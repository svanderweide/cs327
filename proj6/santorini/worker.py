

class SantoriniWorker:

    def __init__(self, name: str, location: tuple) -> None:
        self._name = name
        self._location = location

    def move(self, direction: tuple) -> None:
        print(f'Worker {self._name} moves in direction {direction}')

    def _get_valid_moves(self) -> list[tuple]:
        return None
    
    def build(self, direction: tuple) -> None:
        print(f'Worker {self._name} builds in direction {direction}')
    
    def _get_valid_builds(self) -> list[tuple]:
        return None

    def __str__(self) -> str:
        return f'{self._name}'
