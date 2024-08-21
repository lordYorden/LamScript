class Position:
    def __init__(self, index, ln, col, fn, ftxt):
        """The position of the object in the file
        could be a character, a token, a node, etc.
        Args:
            index (int): the index of the object in the file
            ln (int): the line number
            col (int): the column number
            fn (string): file name
            ftxt (string): file text
        """
        self.index = index
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        """Advance the position of the object in the file

        Args:
            current_char (char, none): the current char that the program reads. Defaults to None.

        Returns:
            Position: the new position of the object
        """
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def backtrack(self, previous_char=None):
        """Backtrack the position of the object in the file

        Args:
            previous_char (char, none): the previous chra that was read. Defaults to None.

        Returns:
            Position: the new position of the object
        """
        self.index -= 1
        self.col -= 1
        
        if previous_char == '\n':
            pass #fix in future
        return self
    
    def extract_str(self, end_pos):
        """Extract the text from the current position to the end position

        Args:
            end_pos (Postion): the end position of the object

        Returns:
            String: the extracted text
        """
        lines = self.ftxt.splitlines()
        
        if self.ln == end_pos.ln:
            return lines[self.ln]

        extracted_text = lines[self.ln] + '\n'

        for line_no in range(self.ln + 1, end_pos.ln):
            extracted_text += lines[line_no] + '\n'

        extracted_text += lines[end_pos.ln]
        return extracted_text
    

    def copy(self):
        """Copies the current position

        Returns:
            Position: The coppied position
        """
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)