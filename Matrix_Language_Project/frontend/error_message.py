class ErrorMessage(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def __str__(self):
        return str(self.lineno)

class UnitializedAccess(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)
        
    def __str__(self):
        return "Accesed uninitialized variable at line: " + super().__str__()

class ListOutOfIndex(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "List out of index at line: " + super().__str__()

class NotIndexable(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Variable not indexable at line: " + super().__str__()

class SizeMismatch(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Matrix initialized with vectors of different sizes at line: " + super().__str__()

class InvalidIndexing(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Indexed with type different than Integer at line: " + super().__str__()

class InvalidInitializer(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Matrix initializer used with type other than integer at line: " + super().__str__()

class TypeMismatch(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Type Mismatch at line: " + super().__str__()

class TypeReassignment(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Type reassignment at line: " + super().__str__()

class KeyWordInstructionOutOfScope(ErrorMessage):
    def __init__(self, lineno):
        super().__init__(lineno)

    def __str__(self):
        return "Used key word statement out of scope at line: " + super().__str__()
