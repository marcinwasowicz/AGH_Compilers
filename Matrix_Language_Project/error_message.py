class ErrorMessage(object):
    def __init__(self, scope):
        self.scope = scope

class UnitializedAccess(ErrorMessage):
    def __init__(self, name, scope):
        super().__init__(scope)
        self.variable_name = name

    def __str__(self):
        return "Accesed uninitialized variable: " + self.variable_name

class ListOutOfIndex(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "List out of index"

class NotIndexable(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "Variable not indexable"

class SizeMismatch(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "Matrix initialized with vectors of different sizes"

class InvalidIndexing(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "Indexed with type different than Integer"

class InvalidInitializer(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "Matrix initializer used with type other than integer"

class TypeMismatch(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "Type Mismatch"

class KeyWordInstructionOutOfScope(ErrorMessage):
    def __init__(self, scope):
        super().__init__(scope)

    def __str__(self):
        return "Used key word statement out of scope"
