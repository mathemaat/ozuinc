from classes.DateParser import DateParser
from classes.Iban import Iban


class InputValidator(object):

    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_date(value):
        try:
            DateParser.parse_from_string(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_iban(value):
        iban = Iban(value)
        return iban.is_valid()
