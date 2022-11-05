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
    return Enigma(swaps=['AZ', 'BQ', 'RS'])

@pytest.fixture
def longtext() -> str:
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" * 26

@pytest.fixture
def longtext_enciphered() -> str:
    return 'BJELRQZVJWARXSNBXORSTNCFMEYYAQUSQSWSQYPAJCKCZEJUDSIUPPTCCBZUHRQRPWJBPCAAZPJZZWDAZIHVYGPITMSRZKGGHLSRBLHLFKELOAYCSWCMUGNZCEDQOMKPEHJZOBRQCMEFNCKSIIZSOMBXUAUXEOVJFROUZGEWFFMEMNIRXPSSCURNHUCVURLZDEGRYNNKVUKMKWMVURTODHRSLTDZGXIIAKWEFHJNLKDAZLBEZPOWJRIONBDQHDVTSTQOCJYNWVXELSDNGRECLKTSIXGEGDCRJEQLXQNCRNQBDRADTYCNFEXDRNPPQOPBYHTASJXOGGVNBLLWNVXHJWDKJQUYXBWKUDYWXCBEOKOJSEAFJCURLYDEGYGNFKEWIUATSOXPJYWKLQEZGTBKCTLJXOKHCEPDJFULQTFMQGFDHDWGMPOPHZOYTRTTMHVPKJRKYOYIRRFBNGPHHADXPVLLFBMEHXWQVWMYOZAZZMTVCGGZHZYJBLKHNFKHQIBSKUBBYARXEPGEFYHINNFPHUMUUPIHESGFVEZVDGUAPCYXRAQGYGNDQIJEFWMVIEPQDBQSUSAYXWTCYOMEZTTOAATIYZNGBVRFBFNPRVUANKPDPYAROIEXVGSJKPRXQPSVJDYKCLUZNWEKBPHRABDAWKVFCNCZICOHLKOJMOQLJIOVUPMWJEAWYUJWDYOQSTQSNSXRJNRBXBWFRHFWGOBSMLALZXGKOGVXHNVICPCZTMQKHDDBMYSFMWGJRSQEYZYHSEBBEEFLQNNKUMHOBBZFHDTRSWLBGGWCZEVIWPMEKIZVDWXOSURRYKNHJJTJLKOJYDMPJMVBWYYIYLDQTBZWYIHMVMLDHGKOIGVIMSJJDDSUPIYOICPBUCXOLPKNGZUOAIPLVFWPKRLVEGGXOIYSFAUVPDOAWKYYKMNCFFWEHUPMUHIEXLZSZXHDHXLJJAYFPEYMQSUYCFWBQCPUJNRCZPJXYLZLTFKNOYURQFZEZUEZIXNLPWKFIERNEMUHVTSRJIIXIFTQVAJMQAEXWLOAFJCDTDFCHHMIBPBMBTOPZHELYARQRNPFZZZSFAFXILFJMOCAQFIQNMQXQTBYNLVHJAGUIPKNEKTLOABAPCYSVACGICKMNMPLHFNEERMWUIYYDAYMYEARABICJJSMBMVZKCKMDLSONUKLQQPSCXAXODKCDWZFPCLLGTATXYQLFOHFLTMAPXQDYYFHHXETGPBXMHJJGPYHICEBLVOLLSJUKXXBWAZQSWPMSSENZKZXJKBWNQLSDVGZXCXKQLRKMTKOHFSFWCWXQLJJIYGDLQLFGKFZJWQRPXHVWPKZWJVRBHAZGBKZGYQR'

class TestEnigma:

    @pytest.mark.parametrize('errval', [['I', 'II', 'IV'], ['I', 'II', 2]])
    def test_enigma_invalid_rotor_key(self, errval):
        with pytest.raises(ValueError):
            Enigma(rotor_order=errval)

    def test_enigma_encipher(self, enigma_default: Enigma, longtext, longtext_enciphered):
        expected = longtext_enciphered
        output = enigma_default.encipher(longtext)
        assert output == expected

    def test_enigma_encode_decode_letter_swaps_lowercase(self, enigma_default_swaps: Enigma):
        expected = 'Q'
        output = enigma_default_swaps.encode_decode_letter('z')
        assert output == expected

    def test_enigma_encode_decode_letter_swaps_double(self, enigma_default_swaps: Enigma):
        expected = 'Q'
        output = enigma_default_swaps.encode_decode_letter('Z')
        assert output == expected

    @pytest.mark.parametrize('errval', ['AB', '2'])
    def test_enigma_encode_decode_letter_err_VE_msg(self, enigma_default: Enigma, errval):
        err_msg = 'Please provide a letter in a-zA-Z.'
        with pytest.raises(ValueError, match=err_msg):
            enigma_default.encode_decode_letter(errval)

    def test_enigma_set_rotor_position_rotors(self, enigma_default: Enigma):
        for rotor in [enigma_default.r_rotor, enigma_default.m_rotor, enigma_default.l_rotor]:
            with patch.object(rotor, 'change_setting'):
                enigma_default.set_rotor_position('ZZZ')
                rotor.change_setting.assert_called_once_with('Z')

    def test_enigma_set_plugs(self, enigma_default_swaps: Enigma):
        expected = {'P': 'Q', 'Q': 'P', 'R': 'S', 'S': 'R'}
        enigma_default_swaps.set_plugs(['PQ', 'RS'], True)
        output = enigma_default_swaps.plugboard.swaps
        assert output == expected

@pytest.fixture
def rotorI() -> Rotor:
    return Rotor('I', 'A')

@pytest.fixture
def rotorV() -> Rotor:
    return Rotor('V', 'Z')

class TestRotor:

    def test_rotorI_encode_letter(self, rotorI: Rotor, capsys):
        expected = (17, '')
        output = (rotorI.encode_letter('X'), capsys.readouterr().out)
        assert output == expected

    def test_rotorI_encode_letter_print(self, rotorI: Rotor, capsys):
        expected = (17, 'Rotor I: input = X, output = R\n')
        output = (rotorI.encode_letter('X', printit=True), capsys.readouterr().out)
        assert output == expected

    def test_rotorV_encode_letter_print(self, rotorV: Rotor, capsys):
        expected = (22, 'Rotor V: input = A, output = V\n')
        output = (rotorV.encode_letter(1, printit=True), capsys.readouterr().out) 
        assert output == expected
