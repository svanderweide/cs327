"""SantoriniBoard testing module"""

import unittest
from unittest.mock import Mock, patch

from santorini.board import SantoriniBoard
from santorini.worker import SantoriniWorker

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

    def test_board_get_tile(self):
        for row in range(self.board._dim[0]):
            for col in range(self.board._dim[1]):
                tile = self.board._tiles[row][col]
                self.assertEqual(self.board._get_tile((row, col)), tile)

class TestMove(unittest.TestCase):

    def setUp(self) -> None:
        self.board = SantoriniBoard()
        self.worker = SantoriniWorker('white', '%', (0, 0))
        self.src = (0, 0)
        self.dst = (1, 1)
        self.board._worker_move(self.worker, self.src)

    def test_board_str_worker_move(self):
        self.board._worker_move(self.worker, self.dst)
        board = ('+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0%|0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+')
        board = '\n'.join(board)
        self.assertEqual(str(self.board), board)
    
    def test_board_worker_move_worker_location(self):
        self.board._worker_move(self.worker, self.dst)
        self.assertEqual(self.worker.location, self.dst)

    def test_board_worker_move_src_tile_worker(self):
        self.board._worker_move(self.worker, self.dst)
        self.assertIsNone(self.board._get_tile(self.src).worker)

    def test_board_worker_move_dst_tile_worker(self):
        self.board._worker_move(self.worker, self.dst)
        self.assertEqual(self.board._get_tile(self.dst).worker, self.worker)

class TestBuild(unittest.TestCase):

    def setUp(self) -> None:
        self.board = SantoriniBoard()
        self.worker = SantoriniWorker('white', '%', (0, 0))
        self.src = (0, 0)
        self.dst = (1, 1)
        self.board._worker_move(self.worker, self.src)

    def test_board_str_worker_build(self):
        self.board._worker_build(self.worker, self.dst)
        board = ('+--+--+--+--+--+',
                 '|0%|0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |1 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+',
                 '|0 |0 |0 |0 |0 |',
                 '+--+--+--+--+--+')
        board = '\n'.join(board)
        self.assertEqual(str(self.board), board)

    def test_board_worker_build(self):
        tile = self.board._get_tile(self.dst)
        with patch.object(tile, 'build') as mock_build:
            self.board._worker_build(self.worker, self.dst)
            mock_build.assert_called_once()

class TestValidation(unittest.TestCase):

    def setUp(self) -> None:
        self.board = SantoriniBoard()
        self.worker = SantoriniWorker('white', '%', (0, 0))
        self.src = (0, 0)
        self.dst = (1, 1)
        self.board._worker_move(self.worker, self.src)

    def test_board_validate_move(self):
        self.assertTrue(self.board._validate_move(self.src, (1, 1)))
    
    def test_board_validate_move_invalid_row(self):
        self.assertFalse(self.board._validate_move(self.src, (-1, 0)))

    def test_board_validate_move_invalid_col(self):
        self.assertFalse(self.board._validate_move(self.src, (0, -1)))

    def test_board_validate_move_invalid_occupied_worker(self):
        self.assertFalse(self.board._validate_move(self.src, self.src))

    def test_board_validate_build(self):
        self.assertTrue(self.board._validate_build((1, 1)))

    def test_board_validate_build_invalid_row(self):
        self.assertFalse(self.board._validate_build((-1, 0)))

    def test_board_validate_build_invalid_col(self):
        self.assertFalse(self.board._validate_build((0, -1)))

    def test_board_validate_build_invalid_occupied_worker(self):
        self.assertFalse(self.board._validate_build(self.src))
