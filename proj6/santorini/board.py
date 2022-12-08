from .board_tile import SantoriniBoardTile

class SantoriniBoard:

    def __init__(self, dim: tuple) -> None:
        self._dim = dim
        self._tiles = self._create_tiles()

    def _create_tiles(self) -> list[list[SantoriniBoardTile]]:
        tiles = []
        for _ in range(self._dim[0]):
            row = []
            for _ in range(self._dim[1]):
                row.append(SantoriniBoardTile())
            tiles.append(row)
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
