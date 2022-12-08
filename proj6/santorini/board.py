from .board_tile import SantoriniBoardTile
from .list_fixed import FixedWidthList
from .architect import SantoriniArchitect
from .player import SantoriniPlayer
from .exceptions import InvalidBuildException, InvalidMoveException
from .constants import DIRECTIONS

class SantoriniBoard:

    def __init__(self, dim: tuple, players: list[SantoriniPlayer]) -> None:
        self._dim = dim
        self._tiles = self._create_tiles()
        self._architects = self._create_architects(players)

    def _create_tiles(self) -> FixedWidthList[FixedWidthList[SantoriniBoardTile]]:
        tiles = FixedWidthList()
        for _ in range(self._dim[0]):
            row = FixedWidthList()
            for _ in range(self._dim[1]):
                row.append(SantoriniBoardTile())
            tiles.append(row)
        return tiles
    
    # only works for 2-player CLI version
    def _create_architects(self, players: list[SantoriniPlayer]) -> dict[str, list[SantoriniArchitect]]:

        cols = [player.col for player in players]

        architects = {}
        for col in cols:

            architects[col]: list[SantoriniArchitect] = []

            # only works for 2-player CLI version
            if col == 'white':
                names = ['A', 'B']
                locations = [(3,1), (1,3)]
            elif col == 'blue':
                names = ['Y', 'Z']
                locations = [(1,1), (3,3)]

            for name, location in zip(names, locations):
                architect = SantoriniArchitect(col, name, location)
                self._tiles[location[1]][location[0]].architect = architect
                architects[col].append(architect)

        return architects

    def get_architects(self, col: str):
        return self._architects.get(col, [])

    def architect_move(self, architect: SantoriniArchitect, direction: str):

        delta = DIRECTIONS[direction]
        
        # locations
        src_location = architect.location
        dst_location = tuple(i + j for i,j in zip(src_location, delta))

        try:
            # tiles
            src_tile: SantoriniBoardTile = self._tiles[src_location[1]][src_location[0]]
            dst_tile: SantoriniBoardTile = self._tiles[dst_location[1]][dst_location[0]]
        except IndexError:
            raise InvalidMoveException()
        else:
            if not src_tile.reaches(dst_tile) or dst_tile.architect is None:
                raise InvalidMoveException()

            # update tiles and architect location
            src_tile.architect = None
            dst_tile.architect = architect
            architect.location = dst_location

    def architect_build(self, architect: SantoriniArchitect, direction: str):

        delta = DIRECTIONS[direction]

        # locations
        src_location = architect.location
        dst_location = tuple(i + j for i,j in zip(src_location, delta))

        print(f'building from {src_location} to {dst_location}')

        try:
            # tiles
            dst_tile: SantoriniBoardTile = self._tiles[dst_location[1]][dst_location[0]]
        except IndexError:
            raise InvalidBuildException()
        else:
            if not dst_tile.architect is None:
                raise InvalidBuildException()
            dst_tile.build()

    def __str__(self) -> str:
        board = ''
        row_division = '+--' * self._dim[1] + '+'

        board += row_division
        for row in range(self._dim[0]):
            board += '\n'
            board += '|'
            for col in range(self._dim[0]):
                board += str(self._tiles[col][row])
                board += '|'
            board += '\n'
            board += row_division

        return board
