"""
testing module for the enigma simulation modules 'machine.py' and 'components.py'
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

    def test_enigma_default_key(self, enigma_default: Enigma):
        assert enigma_default.key == 'AAA'

    def test_enigma_default_swaps(self, enigma_default: Enigma):
        assert repr(enigma_default.plugboard) == repr(Plugboard(None))

    def test_enigma_default_rotor_order(self, enigma_default: Enigma):
        assert enigma_default.rotor_order == ['I', 'II', 'III']

    def test_enigma_repr(self, enigma_default: Enigma):
        repr_str_lst = ['Keyboard <-> Plugboard <->  Rotor I <-> Rotor  II',
                        '<-> Rotor  III <-> Reflector \nKey:  + AAA']
        repr_str = " ".join(repr_str_lst)
        assert repr_str == repr(enigma_default)

    def test_enigma_encipher(self, enigma_default: Enigma, longtext, longtext_enciphered):
        expected = longtext_enciphered
        output = enigma_default.encipher(longtext)
        assert output == expected

    def test_enigma_decipher(self, enigma_default: Enigma, longtext):
        with patch.object(enigma_default, 'encipher'):
            enigma_default.encipher.return_value = ''
            enigma_default.decipher(longtext)
            enigma_default.encipher.assert_called_once_with(longtext)

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

    def test_encode_decode_letter_steps_rotors(self, enigma_default: Enigma):
        with patch.object(enigma_default.r_rotor, 'step'):
            enigma_default.encode_decode_letter('A')
            enigma_default.r_rotor.step.assert_called_once()

    def test_enigma_set_rotor_position_rotors(self, enigma_default: Enigma):
        for rotor in [enigma_default.r_rotor, enigma_default.m_rotor, enigma_default.l_rotor]:
            with patch.object(rotor, 'change_setting'):
                enigma_default.set_rotor_position('ZZZ')
                rotor.change_setting.assert_called_once_with('Z')
    
    def test_enigma_set_rotor_position_invalid(self, enigma_default: Enigma, capsys):
        enigma_default.set_rotor_position(2)
        expected = ('AAA', 'Please provide a three letter position key such as AAA.\n')
        output = (enigma_default.key, capsys.readouterr().out)
        assert output == expected

    def test_enigma_set_rotor_position_print(self, enigma_default: Enigma, capsys):
        enigma_default.set_rotor_position('ZZZ', printIt=True)
        expected = ('ZZZ', 'Rotor position successfully updated. Now using ZZZ.\n')
        output = (enigma_default.key, capsys.readouterr().out)
        assert output == expected

    def test_enigma_set_plugs(self, enigma_default_swaps: Enigma):
        new_swaps = ['PQ', 'RS']
        enigma_default_swaps.set_plugs(new_swaps, replace=True)
        expected = {'P': 'Q', 'Q': 'P', 'R': 'S', 'S': 'R'}
        output = enigma_default_swaps.plugboard.swaps
        assert output == expected

    def test_enigma_set_plugs_print(self, enigma_default_swaps: Enigma, capsys):
        new_swaps = ['PQ', 'RS']
        enigma_default_swaps.set_plugs(new_swaps, replace=True, printIt=True)
        expected = ({'P': 'Q', 'Q': 'P', 'R': 'S', 'S': 'R'},
                    f'Plugboard successfully updated. New swaps are:\nP <-> Q\nR <-> S\n')
        output = (enigma_default_swaps.plugboard.swaps, capsys.readouterr().out)
        assert output == expected

@pytest.fixture
def rotorI() -> Rotor:
    return Rotor('I', 'A')

@pytest.fixture
def rotorV() -> Rotor:
    return Rotor('V', 'Z')

class TestRotor:

    def test_rotor_init_err_VE(self):
        with pytest.raises(ValueError):
            Enigma('IV')

    def test_rotorI_num(self, rotorI: Rotor):
        assert rotorI.rotor_num == 'I'

    def test_rotorI_wiring(self, rotorI: Rotor):
        assert rotorI.wiring == ROTOR_WIRINGS['I']
    
    def test_rotorI_window(self, rotorI: Rotor):
        assert rotorI.window == 'A'

    def test_rotorI_offset(self, rotorI: Rotor):
        assert rotorI.offset == 0

    def test_rotorI_next_rotor_none(self, rotorI: Rotor):
        assert rotorI.next_rotor == None

    def test_rotorI_prev_rotor_none(self, rotorI: Rotor):
        assert rotorI.prev_rotor == None
    
    def test_rotorI_repr(self, rotorI: Rotor):
        repr_str = f"Wiring:\n{ROTOR_WIRINGS['I']}\nWindow: A"
        assert repr_str == repr(rotorI)

    def test_rotorI_step_simple_offset(self, rotorI: Rotor):
        rotorI.step()
        assert rotorI.offset == 1

    def test_rotorI_step_simple_window(self, rotorI: Rotor):
        rotorI.step()
        assert rotorI.window == 'B'

    def test_rotorI_step_next(self, rotorI: Rotor):
        with patch.object(rotorI, 'next_rotor'):
            rotorI.window = rotorI.notch
            rotorI.offset = ALPHABET.index(rotorI.notch) 
            rotorI.step()
            rotorI.next_rotor.step.assert_called_once()
    
    def test_rotorI_step_midrotor(self, rotorI: Rotor):
        with patch.object(rotorI, 'next_rotor'):
            rotorI.next_rotor.window = 'A'
            rotorI.next_rotor.offset = 0
            rotorI.next_rotor.notch = 'A'
            rotorI.step()
            rotorI.next_rotor.step.assert_called_once()

    def test_rotorI_encode_letter(self, rotorI: Rotor, capsys):
        expected = (17, '')
        output = (rotorI.encode_letter('X'), capsys.readouterr().out)
        assert output == expected

    def test_rotorI_encode_letter_backward(self, rotorI: Rotor, capsys):
        expected = (16, '')
        output = (rotorI.encode_letter('X', forward=False), capsys.readouterr().out)
        assert output == expected

    def test_rotorI_encode_letter_return_letter(self, rotorI: Rotor, capsys):
        expected = ('R', '')
        output = (rotorI.encode_letter('X', return_letter=True), capsys.readouterr().out)
        assert output == expected

    def test_rotorI_encode_letter_print(self, rotorI: Rotor, capsys):
        expected = (17, 'Rotor I: input = X, output = R\n')
        output = (rotorI.encode_letter('X', printit=True), capsys.readouterr().out)
        assert output == expected

    def test_rotorV_encode_letter_print(self, rotorV: Rotor, capsys):
        expected = (22, 'Rotor V: input = A, output = V\n')
        output = (rotorV.encode_letter(1, printit=True), capsys.readouterr().out) 
        assert output == expected

    def test_rotorI_encode_letter_next_rotor(self, rotorI: Rotor):
        with patch.object(rotorI, 'next_rotor'):
            rotorI.encode_letter('A', forward=True)
            rotorI.next_rotor.encode_letter.assert_called_once()
    
    def test_rotorI_encode_letter_prev_rotor(self, rotorI: Rotor):
        with patch.object(rotorI, 'prev_rotor'):
            rotorI.encode_letter('A', forward=False)
            rotorI.prev_rotor.encode_letter.assert_called_once()

    def test_rotor_change_setting_window(self, rotorI: Rotor):
        rotorI.change_setting('A')
        assert rotorI.window == 'A'
    
    def test_rotor_change_setting_offset(self, rotorI: Rotor):
        rotorI.change_setting('A')
        assert rotorI.offset == 0

@pytest.fixture
def reflector() -> Reflector:
    return Reflector()

class TestReflector:

    def test_reflector_wiring(self, reflector: Reflector):
        wiring = {'A':'Y', 'B':'R', 'C':'U', 'D':'H', 'E':'Q', 'F':'S', 'G':'L', 'H':'D',
                  'I':'P', 'J':'X', 'K':'N', 'L':'G', 'M':'O', 'N':'K', 'O':'M', 'P':'I',
                  'Q':'E', 'R':'B', 'S':'F', 'T':'Z', 'U': 'C', 'V':'W', 'W':'V', 'X':'J',
                  'Y':'A', 'Z':'T'}
        assert reflector.wiring == wiring

    def test_reflector_repr(self, reflector: Reflector):
        repr_str = f"Reflector wiring: \n{reflector.wiring}"
        assert repr_str == repr(reflector)

@pytest.fixture
def plugboard0() -> Plugboard:
    return Plugboard([])

@pytest.fixture
def plugboard1() -> Plugboard:
    return Plugboard(['AB'])

@pytest.fixture
def plugboard2() -> Plugboard:
    return Plugboard(['AB', 'CD'])

class TestPlugboard:

    def test_plugboard_swaps0(self, plugboard0: Plugboard):
        assert plugboard0.swaps == {}

    def test_plugboard_swaps1(self, plugboard1: Plugboard):
        assert plugboard1.swaps == {'A': 'B', 'B': 'A'}

    def test_plugboard_swaps2(self, plugboard2: Plugboard):
        assert plugboard2.swaps == {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}

    def test_plugboard_repr0(self, plugboard0: Plugboard):
        repr_str = ""
        assert repr_str == repr(plugboard0)
    
    def test_plugboard_repr1(self, plugboard1: Plugboard):
        repr_str = "A <-> B"
        assert repr_str == repr(plugboard1)
    
    def test_plugboard_repr2(self, plugboard2: Plugboard):
        repr_str = "A <-> B\nC <-> D"
        assert repr_str == repr(plugboard2)

    @pytest.mark.parametrize('swaps', [('PQ', 'RS'), {'P': 'Q', 'R': 'S'}, 'PQRS'])
    def test_plugboard_update_swaps_not_list(self, plugboard1: Plugboard, swaps):
        plugboard1.update_swaps(swaps)
        assert plugboard1.swaps == {'A': 'B', 'B': 'A'}

    def test_plugboard_update_swaps(self, plugboard1: Plugboard):
        plugboard1.update_swaps(None, False)
        assert plugboard1.swaps == {'A': 'B', 'B': 'A'}

    def test_plugboard_update_swaps_valid(self, capsys, plugboard1):
        new_swaps = ['CD', 'EF', 'GH', 'IJ', 'KL', 'MN']
        expected = ({'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C', 'E': 'F', 'F': 'E',
                     'G': 'H', 'H': 'G', 'I': 'J', 'J': 'I', 'K': 'L', 'L': 'K',
                     'M': 'N', 'N': 'M'}, '')
        plugboard1.update_swaps(new_swaps)
        output = (plugboard1.swaps, capsys.readouterr().out)
        assert output == expected

    def test_plugboard_update_swaps_invalid(self, capsys, plugboard1):
        new_swaps = ['CD', 'EF', 'GH', 'IJ', 'KL', 'MN', 'OP']
        expected = ({'A': 'B', 'B': 'A'}, 'Only a maximum of 6 swaps is allowed.\n')
        plugboard1.update_swaps(new_swaps)
        output = (plugboard1.swaps, capsys.readouterr().out)
        assert output == expected
