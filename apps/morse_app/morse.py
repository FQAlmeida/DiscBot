import winsound as ws

from apps.morse_app import morse_string_conv
from apps.morse_app import morse_dictonarie


class Morse:
    def __init__(self):
        self.d = morse_dictonarie.Dictonarie()
        self.s = morse_string_conv.StringC()

    def conv(self, frase: str) -> str:
        frase = frase.lower()
        resp = ''
        for x in list(frase):
            x = self.s.tra(x)
            simb = self.d.code(x)
            resp += simb + ' '
        return resp

    @staticmethod
    def getString():
        return input('Digite a frase para converter para morse_app: ').lower()

    @staticmethod
    def beep(morse):
        for x in list(morse):
            if x == '.':
                ws.Beep(400, 100)
            elif x == '-':
                ws.Beep(400, 300)
            elif x == ' ':
                ws.Beep(37, 100)
