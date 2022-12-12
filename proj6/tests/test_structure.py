"""tests the SantoriniStructure class"""

import unittest
from unittest.mock import Mock, patch

from santorini.structure import SantoriniStructure

class TestCore(unittest.TestCase):

    def setUp(self) -> None:
        self.structure = SantoriniStructure()

    def test_structure_initial_level(self):
        assert self.structure._level == 0

    def test_structure_initial_str(self):
        assert str(self.structure) == '0'

    def test_structure_initial_domed(self):
        assert not self.structure.domed()

    def test_structure_build_level(self):
        self.structure.build()
        assert self.structure._level == 1
    
    def test_structure_build_str(self):
        self.structure.build()
        assert str(self.structure) == '1'
    
    def test_structure_domed(self):
        while(self.structure._level != SantoriniStructure._limit_level):
            self.structure.build()
        assert self.structure.domed()
