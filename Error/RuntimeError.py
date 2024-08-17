import string_with_arrows as swa
from Error.Position import Position
from Error.Error import Error

class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context, error_name='Runtime Error'):
        super().__init__(pos_start, pos_end, error_name, details)
        self.context = context
        
    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}"
        result += "\n\n" + swa.string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        #result += f"\nFile {self.pos_start.fn}, line {self.pos_start.ln + 1} col {self.pos_start.col + 1}"
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f"  File {pos.fn}, line {str(pos.ln + 1)} col {str(pos.col + 1)} in {ctx.display_name}\n" + result
            pos = ctx.parent_entry_position
            ctx = ctx.parent

        return "Traceback (most recent call last):\n" + result
    
class TypeError(RunTimeError):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, details, context, 'Type Error')