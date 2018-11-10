import re


class Iban(object):

    PARSE_VALUE_ERROR = 'unable to parse iban'

    BANK_IDENTIFIERS = {
        'INGB': 'INGBNL2A',
        'RABO': 'RABONL2U',
        'ABNA': 'ABNANL2A',
        'ASNB': 'ASNBNL21',
        'SNSB': 'SNSBNL2A',
        'TRIO': 'TRIONL2U',
    }

    def __init__(self, value):
        self.value = value
        self.sanitise()

    def __repr__(self):
        return ' '.join(Iban.chunkify(self.value, 4))

    @staticmethod
    def chunkify(string, chunk_size):
        return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

    def sanitise(self):
        self.value = self.value.replace(' ', '')
        self.value = self.value.upper()

    def get_country_code(self):
        # e.g. 'NL'
        return self.value[:2]

    def get_check_digits(self):
        # e.g. 26
        return int(self.value[2:4])

    def get_bank_code(self):
        # e.g. 'INGB'
        return self.value[4:8]

    def calculate_check_digits(self):
        # start with a code that is the iban with the country code at the end and without the check digits
        code = self.value[4:] + self.get_country_code()
        # replace 'A' by 10, 'B' by 11, ..., 'Y' by 34 and 'Z' by 35
        for i in range(26):
            char = chr(65+i)
            substitute = str(i+10)
            code = code.replace(char, substitute)
        # add two zeroes at the end
        code = int(code) * 100
        # calculate the check digits by applying a modulo operation
        check_digits = 98 - (code % 97)
        return check_digits

    def is_valid(self):
        if len(self.value) != 18:
            return False
        if not re.match(r'^[A-Z]{2}[0-9]{2}[A-Z]{4}[0-9]{10}$', self.value):
            return False
        if self.get_country_code() != 'NL':
            return False
        if self.get_bank_code() not in self.BANK_IDENTIFIERS.keys():
            return False
        if self.calculate_check_digits() != self.get_check_digits():
            return False
        return True

    def get_bic_code(self):
        return self.BANK_IDENTIFIERS[self.get_bank_code()]

    @staticmethod
    def parse_from_string(value):
        iban = Iban(value)
        if iban.is_valid():
            return iban
        else:
            raise ValueError(Iban.PARSE_VALUE_ERROR)
