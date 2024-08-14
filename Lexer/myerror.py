class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}"
        result += f"\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1} col {self.pos_start.col}"
        return result
    
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
    
class IllegalCharacterError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
        
class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)
class TypeError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Type Error', details)

# class RunTimeError(Error):
#     def __init__(self, pos_start, pos_end, details, context):
#         super().__init__(pos_start, pos_end, 'Runtime Error', details)
#         self.context = context

#     def as_string(self):
#         result = self.generate_traceback()
#         result += f"{self.error_name}: {self.details}"
#         result += f"\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1} col {self.pos_start.col}"
#         return result

#     def generate_traceback(self):
#         result = ''
#         pos = self.pos_start
#         ctx = self.context

#         while ctx:
#             result = f"  File {pos.fn}, line {str(pos.ln + 1)} col {str(pos.col)} in {ctx.display_name}\n" + result
#             pos = ctx.parent_entry_pos
#             ctx = ctx.parent

#         return "Traceback (most recent call last):\n" + result