"""SantoriniTile testing module"""

import unittest
from unittest.mock import Mock, patch

from santorini.tile import SantoriniTile
from santorini.worker import SantoriniWorker
from santorini.structure import SantoriniStructure
from santorini.exceptions import InvalidBuildException, InvalidMoveException

class TestCore(unittest.TestCase):

    def setUp(self):
        self._tile = SantoriniTile()

    def test_tile_initial_worker(self):
        self.assertIsNone(self._tile._worker)

    def test_tile_initial_structure(self):
        self.assertEqual(str(self._tile._structure), str(SantoriniStructure()))

    def test_tile_initial_str(self):
        self.assertEqual(str(self._tile), '0 ')

class TestMove(unittest.TestCase):

    def setUp(self):
        self.tile = SantoriniTile()
        self.worker1 = Mock(SantoriniWorker)
    
    def test_tile_set_worker(self):
        self.tile.worker = self.worker1
        self.assertEqual(self.tile.worker, self.worker1)

    def test_tile_set_worker_no_exception(self):
        try:
            self.tile.worker = self.worker1
        except InvalidMoveException:
            self.assertTrue(False)

    def test_tile_set_worker_None(self):
        try:
            self.tile.worker = None
        except InvalidMoveException:
            self.assertTrue(False)

    def test_tile_set_worker_None_occupied(self):
        self.tile.worker = self.worker1
        try:
            self.tile.worker = None
        except InvalidMoveException:
            self.assertTrue(False)

    def test_tile_set_worker_None_domed(self):
        with patch.object(self.tile._structure, 'domed', return_value=True):
            try:
                self.tile.worker = None
            except InvalidMoveException:
                self.assertTrue(False)

    def test_tile_set_worker_exception_occupied(self):
        self.tile.worker = self.worker1
        with self.assertRaises(InvalidMoveException):
            self.tile.worker = self.worker1
    
    def test_tile_set_worker_exception_domed(self):
        with patch.object(self.tile._structure, 'domed', return_value=True):
            with self.assertRaises(InvalidMoveException):
                self.tile.worker = self.worker1

class TestBuild(unittest.TestCase):

    def setUp(self):
        self.tile = SantoriniTile()
        self.worker1 = Mock(SantoriniWorker)
    
    def test_tile_build(self):
        with patch.object(self.tile._structure, 'build') as mock_build:
            self.tile.build()
            mock_build.assert_called_once()   

    def test_tile_build_exception_occupied(self):
        self.tile.worker = self.worker1
        with self.assertRaises(InvalidBuildException):
            self.tile.build()
    
    def test_tile_build_exception_domed(self):
        with patch.object(self.tile._structure, 'domed', return_value=True):
            with self.assertRaises(InvalidBuildException):
                self.tile.build()
