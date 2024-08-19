class Position:
    def __init__(self, index, ln, col, fn, ftxt):
        self.index = index
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def backtrack(self, previous_char=None):
        self.index -= 1
        self.col -= 1
        
        if previous_char == '\n':
            pass #fix in future
        return self
    
    def extract_str(self, end_pos):
        # Collect lines and handle multiline string extraction
        lines = self.ftxt.splitlines()
        
        if self.ln == end_pos.ln:
            return lines[self.ln]

        # First, get the part from the start position to the end of its line
        extracted_text = lines[self.ln] + '\n'#[self.col:] + '\n'

        # Then, get all the lines in between
        for line_no in range(self.ln + 1, end_pos.ln + 1):
            extracted_text += lines[line_no] + '\n'

        # Finally, get the part from the start of the last line to the end position
        extracted_text += lines[end_pos.ln + 1]#[:end_pos.col]
        return extracted_text
    

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)