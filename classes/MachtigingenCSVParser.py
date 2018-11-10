from classes.CSVParser import CSVParser


'''
$clients = array(
  array(
    'id'        => 123456,                     // knsb-nummer
    'name'      => 'Jan Alleman',
    'mandate'   => 1,                          // volgnummer machtiging
    'signature' => '2017-01-01',               // datum machtiging
    'bic'       => 'INGBNL2A',
    'iban'      => 'NL99INGB0123456789',
    'lid'       => 'senior hoofdlidmaatschap', // omschrijving op bankafschrift
    'amount'    => 50.00
  ),
);
'''

class MachtigingenCSVParser(CSVParser):

    # definieer kolomnummers
    KOLOM_MANDAAT_ID = 0
    KOLOM_DATUM_HANDTEKENING = 1
    KOLOM_BEDRAG = 2
    KOLOM_IBAN = 3
    KOLOM_KNSB_NUMMER = 5
    KOLOM_TEN_NAME_VAN = 6
    KOLOM_LIDMAATSCHAP = 16

    def set_column_definitions(self):
        self.column_definitions = {
            self.KOLOM_MANDAAT_ID: CSVParser.TYPE_INTEGER,
            self.KOLOM_DATUM_HANDTEKENING: CSVParser.TYPE_DATE,
            self.KOLOM_BEDRAG: CSVParser.TYPE_FLOAT,
            self.KOLOM_IBAN: CSVParser.TYPE_IBAN,
            self.KOLOM_TEN_NAME_VAN: CSVParser.TYPE_STRING,
            self.KOLOM_KNSB_NUMMER: CSVParser.TYPE_INTEGER,
            self.KOLOM_LIDMAATSCHAP: CSVParser.TYPE_STRING,
        }

    def validate(self):
        pass
