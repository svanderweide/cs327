import unittest
from unittest.mock import Mock, patch

from santorini.worker import SantoriniWorker

class TestUnit(unittest.TestCase):

    def setUp(self) -> None:
        self.worker1 = SantoriniWorker('white', 'A')

    def test_worker_col(self):
        self.assertEqual(self.worker1._col, 'white')

    def test_worker_name(self):
        self.assertEqual(self.worker1._name, 'A')

    def test_worker_str(self):
        self.assertEqual(str(self.worker1), 'A')

    def test_worker_default_location(self):
        self.assertEqual(self.worker1.location, ())

    def test_worker_set_location(self):
        location = (5, 4)
        self.worker1.location = location
        self.assertEqual(self.worker1.location, location)
