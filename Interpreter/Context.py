from Interpreter.SymbolTable import SymbolTable
class Context:
    def __init__(self, display_name, parent=None, parent_entry_position=None):
        self.display_name = display_name
        self.parent = parent
        self.symbol_table = None
        if parent:
            self.symbol_table = SymbolTable(parent.symbol_table)
        self.parent_entry_position = parent_entry_position
        
    def set_perent(self, parent):
        self.parent = parent
        return self
        
    