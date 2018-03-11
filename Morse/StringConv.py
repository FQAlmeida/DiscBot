class StringC:
    @staticmethod
    def tra(x):
        string = \
            {
                'ç': 'c',
                'é': 'e',
                'í': 'i'
            }
        try:
            return string[x]
        except:
            return x
