import configparser
import unittest

from apps.gw2_app.apitoken import api_token
from apps.morse_app.morse import Morse
from os import environ 

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
        try:
            configs = configparser.ConfigParser()
            configs.read("../data/configs.ini")
            token = configs["GW2"].get("my_token")
        except:
            token = environ.get("GW2_TOKEN")
        check = api_token.check_token(token)
        self.assertTrue(check)
        values = (True, token, ['tradingpost', 'characters', 'pvp', 'progression', 'wallet', 'guilds', 'builds', 'account', 'inventories', 'unlocks'])
        self.assertEqual(check, values)
        

def _run_test() -> unittest.TestProgram:
    return unittest.main()


def get_result():
    return _run_test().result
