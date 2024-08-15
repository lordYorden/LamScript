class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.perent = None
        
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.perent:
            return self.perent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
        
    def remove(self, name):
        del self.symbols[name]
        
    