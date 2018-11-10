import csv
import io

from classes.DateParser import DateParser
from classes.Iban import Iban


class CSVParser(object):

    TYPE_STRING = 0
    TYPE_INTEGER = 1
    TYPE_FLOAT = 2
    TYPE_DATE = 3
    TYPE_IBAN = 4

    def __init__(self, data, has_header = True):
        self.data = data
        self.has_header = has_header
        self.column_definitions = []
        self.header_row = None
        self.rows = []
        self.dirty_cells = []
        self.validation_errors = []

        self.csv2rows()
        self.set_column_definitions()
        self.sanitise()

    def csv2rows(self):
        with io.StringIO(self.data) as csvfile:
            twolines = csvfile.readline() + '\n' + csvfile.readline()
            dialect = csv.Sniffer().sniff(twolines, delimiters=",;")
            csvfile.seek(0)
            reader = csv.reader(csvfile, dialect)
            firstrow = True
            for row in reader:
                if self.has_header and firstrow:
                    self.header_row = row
                    firstrow = False
                else:
                    self.rows.append(row)

    def set_column_definitions(self):
        raise NotImplementedError('Abstract function not implemented')

    def sanitise(self):
        for rowno, cells in enumerate(self.rows):
            for colno, value in enumerate(cells):
                if colno in self.column_definitions:
                    # cast string value to appropriate data type
                    try:
                        if self.column_definitions[colno] == self.TYPE_INTEGER:
                            self.rows[rowno][colno] = int(value)
                        elif self.column_definitions[colno] == self.TYPE_FLOAT:
                            self.rows[rowno][colno] = float(value)
                        elif self.column_definitions[colno] == self.TYPE_DATE:
                            self.rows[rowno][colno] = DateParser.parse_from_string(value)
                        elif self.column_definitions[colno] == self.TYPE_IBAN:
                            self.rows[rowno][colno] = Iban.parse_from_string(value)
                    except ValueError:
                        self.dirty_cells.append((rowno, colno))
                else:
                    # clear irrelevant cells
                    self.rows[rowno][colno] = None

    def is_clean(self):
        return len(self.dirty_cells) == 0

    def validate(self):
        raise NotImplementedError('Abstract function not implemented')

    def is_valid(self):
        return len(self.validation_errors) == 0

    def get_sanitisation_errors(self):
        error_messages = []
        for cell in self.dirty_cells:
            rowno, colno = cell
            if self.column_definitions[colno] == self.TYPE_INTEGER:
                error_message = 'ongeldig geheel getal ' + self.rows[rowno][colno]
            elif self.column_definitions[colno] == self.TYPE_FLOAT:
                error_message = 'ongeldig decimaal getal ' + self.rows[rowno][colno]
            elif self.column_definitions[colno] == self.TYPE_DATE:
                error_message = 'ongeldige datum ' + self.rows[rowno][colno]
            elif self.column_definitions[colno] == self.TYPE_IBAN:
                error_message = 'ongeldige iban ' + self.rows[rowno][colno]
            else:
                error_message = ''
            if len(error_message) >= 1:
                error_message += ' in rij {0}, kolom {1}'.format(rowno + 1, colno + 1)
                error_messages.append(error_message)
        return error_messages
