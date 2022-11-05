"""
testing module for the enigma1 simulation modules 'machine.py' and 'components.py'
"""

# testing modules
import pytest
from unittest.mock import patch

# under-test modules
from machine import Enigma
from components import ALPHABET, ROTOR_WIRINGS, ROTOR_NOTCHES, Rotor, Reflector, Plugboard

class TestConstants:

    def test_rotor_wiring1(self):
        wiring = {'forward':'EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'backward':'UWYGADFPVZBECKMTHXSLRINQOJ'}
        assert ROTOR_WIRINGS['I'] == wiring

    def test_rotor_wiring2(self):
        wiring = {'forward':'AJDKSIRUXBLHWTMCQGZNPYFVOE', 'backward':'AJPCZWRLFBDKOTYUQGENHXMIVS'}
        assert ROTOR_WIRINGS['II'] == wiring
    
    def test_rotor_wiring3(self):
        wiring = {'forward':'BDFHJLCPRTXVZNYEIWGAKMUSQO', 'backward':'TAGBPCSDQEUFVNZHYIXJWLRKOM'}
        assert ROTOR_WIRINGS['III'] == wiring

    def test_rotor_wiring5(self):
        wiring = {'forward':'VZBRGITYUPSDNHLXAWMJQOFECK', 'backward':'QCYLXWENFTZOSMVJUDKGIARPHB'}
        assert ROTOR_WIRINGS['V'] == wiring

    def test_rotor_notches(self):
        assert ROTOR_NOTCHES == {'I': 'Q', 'II': 'E', 'III': 'V', 'V': 'Z'}

    def test_rotor_alphabet(self):
        assert ALPHABET == 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
