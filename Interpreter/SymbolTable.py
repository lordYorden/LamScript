class SymbolTable:
    def __init__(self, parent=None):
        """Initializes the SymbolTable object

        Args:
            parent (SymbolTable, None): the parent symbol table. Defaults to None.
        """
        self.symbols = {}
        self.perent = parent
        
    def get(self, name):
        """Gets the object of a symbol

        Args:
            name (String): the name of the symbol

        Returns:
            Object: the object of the symbol
        """
        value = self.symbols.get(name, None)
        if value == None and self.perent:
            return self.perent.get(name)
        return value
    
    def set(self, name, value):
        """Sets the object of a symbol

        Args:
            name (String): the name of the symbol
            value (Object): the object of the symbol
        """
        self.symbols[name] = value
        
    def remove(self, name):
        """Removes a symbol

        Args:
            name (String): the name of the symbol
        """
        del self.symbols[name]
        
    