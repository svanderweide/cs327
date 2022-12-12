"""SantoriniBoard testing module"""

import unittest
from unittest.mock import Mock, patch

from santorini.board import SantoriniBoard
from santorini.exceptions import InvalidBuildException, InvalidMoveException

class TestCore(unittest.TestCase):

    def setUp(self) -> None:
        self.board = SantoriniBoard((5, 5))
    
    def test_board_dim_row(self):
        self.assertEqual(self.board._dim[0], 5)

    def test_board_dim_col(self):
        self.assertEqual(self.board._dim[1], 5)

    def test_board_str(self):
        board = ('+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+')
        board = '\n'.join(board)
        self.assertEqual(str(self.board), board)
