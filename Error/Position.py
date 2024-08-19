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

        lines = self.ftxt.splitlines()
        
        if self.ln == end_pos.ln:
            return lines[self.ln]

        extracted_text = lines[self.ln] + '\n'

        for line_no in range(self.ln + 1, end_pos.ln):
            extracted_text += lines[line_no] + '\n'

        extracted_text += lines[end_pos.ln]
        return extracted_text
    

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)