import configparser
import unittest

from gw2_app.apitoken import api_token
from morse_app.morse import Morse


class TestDiscBot(unittest.TestCase):
    def test_morse_test(self):
        morse = Morse()
        string = "Hello World!"
        self.assertEqual(morse.conv(string), ".... . .-.. .-.. ---         .-- --- .-. .-.. -.. -.-.-- ")

    @unittest.skip("WIP")
    def test_morse_hard_test(self):
        morse = Morse()
        string = "Hello World!"
        self.assertEqual(morse.conv(string), "")

    def test_check_token_gw2(self):
        configs = configparser.ConfigParser()
        configs.read("../data/configs.ini")
        token = configs["GW2"].get("my_token")
        check = api_token.check_token(token)
        self.assertTrue(check)
        values = (True, 'B3467095-168A-DD4A-93A8-3BA83F186C83', ['tradingpost', 'characters', 'pvp', 'progression', 'wallet', 'guilds', 'builds', 'account', 'inventories', 'unlocks'])
        self.assertEqual(check, values)


def _run_test() -> unittest.TestProgram:
    return unittest.main()


def get_result():
    return _run_test().result
