class Node(object):
    pass

class Integer(Node):
    def __init__(self, value):
        self.value = value

class Float(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name, lineno):
        self.name = name
        self.lineno = lineno

class UnaryVariable(Node):
    def __init__(self, operator, value):
        self.operator = operator
        self.value = value

class MatrixInitializer(Node):
    def __init__(self, keyword, operation, lineno):
        self.keyword = keyword
        self.operation = operation
        self.lineno = lineno

class Sequence(Node):
    def __init__(self, elements=None):
       self.elements = elements

class List(Node):
    def __init__(self, sequence, lineno):
        self.sequence = sequence
        self.lineno = lineno

class MatrixElement(Node):
    def __init__(self, identifier, indexing_sequence, lineno):
        self.identifier = identifier
        self.indexing_sequence = indexing_sequence
        self.lineno = lineno

class KeyWordInstruction(Node):
    def __init__(self, keyword, lineno, continuation=None):
        self.keyword = keyword
        self.continuation = continuation
        self.lineno = lineno

class Assignment(Node):
    def __init__(self, lvalue, operator, operation, lineno):
        self.lvalue = lvalue
        self.operator = operator
        self.operation = operation
        self.lineno = lineno

class Operation(Node):
    def __init__(self, operator, left, right, lineno):
        self.operator = operator
        self.left = left
        self.right = right
        self.lineno = lineno

class Condition(Node):
    def __init__(self, operator, left, right, lineno):
        self.operator = operator
        self.left = left
        self.right = right
        self.lineno = lineno

class ForLooping(Node):
    def __init__(self, iterator, start, end, body):
        self.iterator = iterator
        self.start = start
        self.end = end
        self.body = body

class WhileLooping(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IfStatement(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class Actions(Node):
    def __init__(self, series):
        self.series = series
