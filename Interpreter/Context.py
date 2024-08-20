from Interpreter.SymbolTable import SymbolTable
class Context:
    def __init__(self, display_name, parent=None, parent_entry_position=None):
        """Initializes the context object

        Args:
            display_name (String): the name of the context
            parent (Context, None): the parent context. Defaults to None.
            parent_entry_position (Position, None): the new context entry position. Defaults to None.
        """
        self.display_name = display_name
        self.parent = parent
        self.symbol_table = None
        if parent:
            self.symbol_table = SymbolTable(parent.symbol_table)
        self.parent_entry_position = parent_entry_position
        
    def set_perent(self, parent):
        """Sets the parent context

        Args:
            parent (Context): the parent context

        Returns:
            Context: the current context object
        """
        self.parent = parent
        return self
        
    