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
    def __init__(self, name):
        self.name = name

class UnaryVariable(Node):
    def __init__(self, operator, value):
        self.operator = operator
        self.value = value

class MatrixInitializer(Node):
    def __init__(self, keyword, operation):
        self.keyword = keyword
        self.operation = operation

class Sequence(Node):
    def __init__(self, head, tail=None):
        self.head = head
        self.tail = tail

class List(Node):
    def __init__(self, sequence):
        self.sequence = sequence

class MatrixElement(Node):
    def __init__(self, identifier, indexing_sequence):
        self.identifier = identifier
        self.indexing_sequence = indexing_sequence

class KeyWordInstruction(Node):
    def __init__(self, keyword, continuation=None):
        self.keyword = keyword
        self.continuation = continuation

class Assignment(Node):
    def __init__(self, lvalue, operator, operation):
        self.lvalue = lvalue
        self.operator = operator
        self.operation = operation

class Operation(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

class Condition(Node):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

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






