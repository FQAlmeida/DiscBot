from morse.dictonarie import Dictonarie
from morse.string_conv import StringC
import winsound as ws


class Morse:
    def __init__(self):
        self.d = Dictonarie()
        self.s = StringC()

    def conv(self, frase):
        resp = ''
        for x in list(frase):
            x = self.s.tra(x)
            morse = self.d.code(x)
            resp += morse + ' '
        return resp

    @staticmethod
    def getString():
        return input('Digite a frase para converter para morse: ').lower()

    @staticmethod
    def beep(morse):
        for x in list(morse):
            if x == '.':
                ws.Beep(400, 100)
            elif x == '-':
                ws.Beep(400, 300)
            elif x == ' ':
                ws.Beep(37, 100)
