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

@pytest.fixture
def enigma_default() -> Enigma:
    return Enigma()

@pytest.fixture
def enigma_default_swaps() -> Enigma:
    return Enigma(swaps=['AB', 'TG', 'XY'])

@pytest.fixture
def longtext() -> str:
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" * 26

@pytest.fixture
def longtext_enciphered() -> str:
    return 'BJELRQZVJWARXSNBXORSTNCFMEYYAQUSQSWSQYPAJCKCZEJUDSIUPPTCCBZUHRQRPWJBPCAAZPJZZWDAZIHVYGPITMSRZKGGHLSRBLHLFKELOAYCSWCMUGNZCEDQOMKPEHJZOBRQCMEFNCKSIIZSOMBXUAUXEOVJFROUZGEWFFMEMNIRXPSSCURNHUCVURLZDEGRYNNKVUKMKWMVURTODHRSLTDZGXIIAKWEFHJNLKDAZLBEZPOWJRIONBDQHDVTSTQOCJYNWVXELSDNGRECLKTSIXGEGDCRJEQLXQNCRNQBDRADTYCNFEXDRNPPQOPBYHTASJXOGGVNBLLWNVXHJWDKJQUYXBWKUDYWXCBEOKOJSEAFJCURLYDEGYGNFKEWIUATSOXPJYWKLQEZGTBKCTLJXOKHCEPDJFULQTFMQGFDHDWGMPOPHZOYTRTTMHVPKJRKYOYIRRFBNGPHHADXPVLLFBMEHXWQVWMYOZAZZMTVCGGZHZYJBLKHNFKHQIBSKUBBYARXEPGEFYHINNFPHUMUUPIHESGFVEZVDGUAPCYXRAQGYGNDQIJEFWMVIEPQDBQSUSAYXWTCYOMEZTTOAATIYZNGBVRFBFNPRVUANKPDPYAROIEXVGSJKPRXQPSVJDYKCLUZNWEKBPHRABDAWKVFCNCZICOHLKOJMOQLJIOVUPMWJEAWYUJWDYOQSTQSNSXRJNRBXBWFRHFWGOBSMLALZXGKOGVXHNVICPCZTMQKHDDBMYSFMWGJRSQEYZYHSEBBEEFLQNNKUMHOBBZFHDTRSWLBGGWCZEVIWPMEKIZVDWXOSURRYKNHJJTJLKOJYDMPJMVBWYYIYLDQTBZWYIHMVMLDHGKOIGVIMSJJDDSUPIYOICPBUCXOLPKNGZUOAIPLVFWPKRLVEGGXOIYSFAUVPDOAWKYYKMNCFFWEHUPMUHIEXLZSZXHDHXLJJAYFPEYMQSUYCFWBQCPUJNRCZPJXYLZLTFKNOYURQFZEZUEZIXNLPWKFIERNEMUHVTSRJIIXIFTQVAJMQAEXWLOAFJCDTDFCHHMIBPBMBTOPZHELYARQRNPFZZZSFAFXILFJMOCAQFIQNMQXQTBYNLVHJAGUIPKNEKTLOABAPCYSVACGICKMNMPLHFNEERMWUIYYDAYMYEARABICJJSMBMVZKCKMDLSONUKLQQPSCXAXODKCDWZFPCLLGTATXYQLFOHFLTMAPXQDYYFHHXETGPBXMHJJGPYHICEBLVOLLSJUKXXBWAZQSWPMSSENZKZXJKBWNQLSDVGZXCXKQLRKMTKOHFSFWCWXQLJJIYGDLQLFGKFZJWQRPXHVWPKZWJVRBHAZGBKZGYQR'

class TestEnigma:

    def test_enigma_encipher(self, enigma_default: Enigma, longtext, longtext_enciphered):
        expected = longtext_enciphered
        output = enigma_default.encipher(longtext)
        assert output == expected

    def test_enigma_encode_decode_letter_swaps(self, enigma_default_swaps: Enigma):
        expected = 'Y'
        output = enigma_default_swaps.encode_decode_letter('T')
        assert output == expected

@pytest.fixture
def rotor1() -> Rotor:
    return Rotor('I', 'A')

class TestRotor:

    def test_rotor_encode_letter_print_false(self, rotor1, capsys):
        expected = (17, '')
        output = (rotor1.encode_letter('X'), capsys.readouterr().out)
        assert output == expected

    def test_rotor_encode_letter_print_true(self, rotor1, capsys):
        expected = (17, 'Rotor I: input = X, output = R\n')
        output = (rotor1.encode_letter('X', printit=True), capsys.readouterr().out)
        assert output == expected
