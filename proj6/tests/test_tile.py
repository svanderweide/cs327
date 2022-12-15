"""SantoriniTile testing module"""

import unittest
from unittest.mock import Mock, patch

from santorini.tile import SantoriniTile

class TestCore(unittest.TestCase):

    def setUp(self):
        self.tile = SantoriniTile()

    def test_tile_initial_worker(self):
        self.assertIsNone(self.tile._worker)

    def test_tile_initial_level(self):
        self.assertEqual(self.tile._level, 0)

    def test_tile_initial_str(self):
        self.assertEqual(str(self.tile), '0 ')

    def test_tile_worker_get(self):
        self.assertIsNone(self.tile.worker)
    
    def test_tile_worker_set(self):
        work = Mock()
        self.tile.worker = work
        self.assertEqual(self.tile.worker, work)

    def test_tile_str_level(self):
        self.tile._level = 1
        self.assertEqual(str(self.tile), '1 ')

    def test_tile_str_worker(self):
        work = Mock()
        with patch.object(work, '__str__', return_value='A'):
            self.tile.worker = work
            self.assertEqual(str(self.tile), '0A')
    
    def test_tile_build(self):
        level = self.tile._level
        self.tile.build()
        self.assertEqual(self.tile._level, level + 1)

    def test_tile_undo_build(self):
        level = self.tile._level
        self.tile.build()
        self.tile.undo_build()
        self.assertEqual(self.tile._level, level)

class TestMultiple(unittest.TestCase):

    def setUp(self) -> None:
        self.tile1 = SantoriniTile()
        self.tile2 = SantoriniTile()

    def test_tile_reaches_same_level(self):
        self.assertTrue(self.tile1.reaches(self.tile2))

    def test_tile_reaches_up_1(self):
        self.tile2.build()
        self.assertTrue(self.tile1.reaches(self.tile2))
    
    def test_tile_reaches_up_2(self):
        self.tile2.build()
        self.tile2.build()
        self.assertFalse(self.tile1.reaches(self.tile2))

    def test_tile_reaches_down_max(self):
        self.tile1._level = SantoriniTile._limit_level
        self.assertTrue(self.tile1.reaches(self.tile2))
