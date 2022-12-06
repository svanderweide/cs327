"""Santorini game board module"""

from santorini.board_tile import SantoriniBoardTile

class SantoriniBoard:
    """Santorini game board class"""

    def __init__(self, dim: int) -> None:
        self._dim: tuple = (dim, dim)
        self._tiles = self._construct_board()

    def _construct_board(self):
        return self._construct_board_section(self._dim)

    def _construct_board_section(self, dim: tuple) -> list[SantoriniBoardTile] | SantoriniBoardTile:
        if dim:
            section = []
            for _ in range(dim[0]):
                subsection = self._construct_board_section(dim[1:])
                section.append(subsection)
        else:
            section = SantoriniBoardTile()
        return section

    def __str__(self) -> None:
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
