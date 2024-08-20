from Interpreter.Context import Context
import string_with_arrows as swa
from Error.Position import Position

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        """The error class

        Args:
            pos_start (Position): the start position of the error
            pos_end (Position): the end position of the error
            error_name (String): the name of the error
            details (String): the details of the error
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        """The string representation of the error

        Returns:
            String: the string representation of the error
        """
        result = f"{self.error_name}: {self.details}"
        result += f"\nFile {self.pos_end.fn}, line {self.pos_end.ln + 1} col {self.pos_end.col}"
        result += "\n\n" + swa.string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    
class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end, details):
        """The illegal character error class

        Args:
            pos_start (Position): the start position of the error
            pos_end (Position): the end position of the error
            details (String): the details of the error
        """
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        """The invalid syntax error class

        Args:
            pos_start (Position): the start position of the error
            pos_end (Position): the end position of the error
            details (String): the details of the error
        """
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        """The expected character error class

        Args:
            pos_start (Position): the start position of the error
            pos_end (Position): the end position of the error
            details (String): the details of the error
        """
        super().__init__(pos_start, pos_end, 'Expected Character', details)