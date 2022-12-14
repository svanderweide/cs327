"""SantoriniWorker testing module"""

import unittest
from unittest.mock import Mock, patch

from santorini.worker import SantoriniWorker

class TestCore(unittest.TestCase):

    def setUp(self) -> None:
        self.worker = SantoriniWorker('white', 'A')

    def test_worker_col(self):
        self.assertEqual(self.worker._col, 'white')

    def test_worker_name(self):
        self.assertEqual(self.worker._name, 'A')

    def test_worker_str(self):
        self.assertEqual(str(self.worker), 'A')

    def test_worker_default_location(self):
        self.assertEqual(self.worker.location, (0, 0))

    def test_worker_set_location(self):
        location = (5, 4)
        self.worker.location = location
        self.assertEqual(self.worker.location, location)
