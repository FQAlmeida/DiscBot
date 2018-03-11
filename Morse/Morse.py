from Morse.Dictonarie import Dictonarie as d
from Morse.StringConv import StringC as s
import winsound as ws


class Morse:
    @staticmethod
    def conv(frase):
        resp = ''
        for x in list(frase):
            x = s.tra(x)
            morse = d.code(d, x)
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
