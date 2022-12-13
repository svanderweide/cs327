"""SantoriniBoard testing module"""

import unittest
from unittest.mock import Mock, patch

from santorini.board import SantoriniBoard
from santorini.tile import SantoriniTile
from santorini.worker import SantoriniWorker
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
                 '|0 |0Y|0 |0B|0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0A|0 |0Z|0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+')
        board = '\n'.join(board)
        self.assertEqual(str(self.board), board)

class TestMove(unittest.TestCase):

    def setUp(self) -> None:
        self.board = SantoriniBoard((5, 5))
        self.worker = SantoriniWorker('white', '$')

    def test_board_worker_move_tile_update(self):
        tile: SantoriniTile = self.board._get_tile((2, 2))
        self.board.worker_move(self.worker, (2, 2))
        self.assertEqual(tile.worker, self.worker)

    def test_board_worker_move_worker_update(self):
        self.board.worker_move(self.worker, (2, 2))
        self.assertEqual(self.worker.location, (2, 2))

    def test_board_worker_move_board_str(self):
        self.board.worker_move(self.worker, (2, 2))
        board = ('+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0Y|0 |0B|0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0$|0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0A|0 |0Z|0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+')
        board = '\n'.join(board)
        self.assertEqual(str(self.board), board)

    def test_board_worker_move_exception_negative_row(self):
        self.board.worker_move(self.worker, (0, 0))
        with self.assertRaises(InvalidMoveException):
            self.board.worker_move(self.worker, (-1, 0))

    def test_board_worker_move_exception_negative_col(self):
        self.board.worker_move(self.worker, (0, 0))
        with self.assertRaises(InvalidMoveException):
            self.board.worker_move(self.worker, (0, -1))

    def test_board_worker_move_exception_too_high(self):
        self.board.worker_move(self.worker, (0, 0))
        tile: SantoriniTile = self.board._get_tile((0, 1))
        for _ in range(2):
            tile.build()
        with self.assertRaises(InvalidMoveException):
            self.board.worker_move(self.worker, (0, 1))

class TestBuild(unittest.TestCase):

    def setUp(self) -> None:
        self.board = SantoriniBoard((5, 5))
        self.worker = SantoriniWorker('white', '$')
    
    def test_board_worker_build_tile_update(self):
        tile = self.board._get_tile((2, 2))
        self.board.worker_move(self.worker, (1, 2))
        with patch.object(tile, 'build') as mock_build:
            self.board.worker_build(self.worker, (1, 0))
            mock_build.assert_called_once()

    def test_board_worker_build_board_str(self):
        self.board.worker_move(self.worker, (1, 2))
        self.board.worker_build(self.worker, (1, 0))
        board = ('+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0Y|0$|0B|0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |1 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0A|0 |0Z|0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+')
        board = '\n'.join(board)
        self.assertEqual(str(self.board), board)

    def test_board_worker_build_exception_negative_row(self):
        self.board.worker_move(self.worker, (0, 0))
        with self.assertRaises(InvalidBuildException):
            self.board.worker_build(self.worker, (-1, 0))

    def test_board_worker_build_exception_negative_col(self):
        self.board.worker_move(self.worker, (0, 0))
        with self.assertRaises(InvalidBuildException):
            self.board.worker_build(self.worker, (0, -1))
