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
    

    def copy(self):
        return Position(self.index, self.ln, self.col, self.fn, self.ftxt)