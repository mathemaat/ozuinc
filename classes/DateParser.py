from datetime import date


class DateParser(object):

    PARSE_VALUE_ERROR = 'unable to parse date'

    @staticmethod
    def parse_from_string(value):
        success = False
        for separator in ['-', '/']:
            units = value.split(separator)
            if len(units) == 3:
                success = True
                break
        if not success:
            raise ValueError(DateParser.PARSE_VALUE_ERROR)
        try:
            year = int(units[2])
            month = int(units[1])
            day = int(units[0])
            return date(year, month, day)
        except ValueError:
            raise ValueError(DateParser.PARSE_VALUE_ERROR)
