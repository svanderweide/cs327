from .board_tile import SantoriniBoardTile

class SantoriniBoard:

    def __init__(self, dim: tuple=None) -> None:
        self._dim: tuple = dim if dim else (5,5)
        self._tiles: list = self._create_tiles()

    def _create_tiles(self) -> list:
        row = [SantoriniBoardTile() for _ in range(self._dim[1])]
        tiles = [list(row) for _ in range(self._dim[0])]
        return tiles

    def __str__(self) -> str:
        board = ''
        row_division = '+--' * self._dim[1] + '+'

        board += row_division
        for row in range(self._dim[0]):
            board += '\n'
            board += '|'
            for col in range(self._dim[0]):
                board += str(self._tiles[row][col])
                board += '|'
            board += '\n'
            board += row_division

        return board
