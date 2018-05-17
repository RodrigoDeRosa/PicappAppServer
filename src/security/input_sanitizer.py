from src.utils.logger_config import Logger


class InvalidFormatException(Exception):
    def __init__(self, got, expected):
        self.message = str(got)+" is not a "+str(expected)
        self.error_code = 400

    def __str__(self):
        return self.message


class InputSanitizer(object):

    @staticmethod
    def sanitize_boolean(input_data):
        if input_data in ['true', 'True', True]:
            Logger(__name__).info('Input {} recognized as boolean True.'.format(str(input_data)))
            return True
        if input_data in ['false', 'False', False]:
            Logger(__name__).info('Input {} recognized as boolean False.'.format(str(input_data)))
            return False
        Logger(__name__).info('Input {} not recognized as a boolean.'.format(str(input_data)))
        raise InvalidFormatException(input_data, "boolean")

    @staticmethod
    def sanitize_integer(input_data):
        try:
            sanitized_data = int(input_data)
            Logger(__name__).info('Input {} successfully recognized as an integer.'.
                                  format(str(input_data)))
            return sanitized_data
        except ValueError:
            Logger(__name__).info('Input {} not recognized as an integer.'.format(str(input_data)))
            raise InvalidFormatException(input_data, "integer")
