
class IntFloatStringConverter:
    @staticmethod
    def __isfloat(x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    @staticmethod
    def __isint(x):
        try:
            a = float(x)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b

    @staticmethod
    def convert(x):
        if IntFloatStringConverter.__isint(x):
            return int(x)
        elif IntFloatStringConverter.__isfloat(x):
            return float(x)
        else:
            return str(x)
