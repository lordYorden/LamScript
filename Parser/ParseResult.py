class ParseResult:
    
    def __init__(self):
        """The parse result"""
        self.error = None
        self.node = None
        self.advance_count = 0
    
    def register(self, res):
        """Register the result of the parse.

        Args:
            res (ParseResult): the result of the parse

        Returns:
            BaseNode: the node returned from the parse
        """
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
    
    def register_advancement(self):
        """Register the advancement of the parse.

        Returns:
            ParseResult: the new ParseResult of the parser
        """
        self.advance_count += 1
        return self
    
    def success(self, node):
        """Register the success of the parse.

        Args:
            node (BaseNode): the node of the parse

        Returns:
            ParseResult: the new ParseResult of the parser
        """
        self.node = node
        return self
    
    def failure(self, error):
        """Register the failure of the parse.

        Args:
            error (error): the error of the parse

        Returns:
            ParseResult: the new ParseResult of the parse
        """
        if not self.error or self.advance_count == 0:
            self.error = error
        return self