from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Integer)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.Float)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("| " * indent + self.name)

    @addToClass(AST.UnaryVariable)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.value.printTree(indent)

    @addToClass(AST.MatrixInitializer)
    def printTree(self, indent=0):
        print("| " * indent + self.keyword)
        self.operation.printTree(indent + 1)

    @addToClass(AST.Sequence)
    def printTree(self, indent=0):
        self.head.printTree(indent)
        if self.tail is not None:
            self.tail.printTree(indent)

    @addToClass(AST.List)
    def printTree(self, indent=0):
        print("| " * indent, "VECTOR")
        self.sequence.printTree(indent+1)

    @addToClass(AST.MatrixElement)
    def printTree(self, indent=0):
        print("| " * indent  + "REF")
        self.identifier.printTree(indent+1)
        self.indexing_sequence.printTree(indent+1)

    @addToClass(AST.KeyWordInstruction)
    def printTree(self, indent=0):
        print("| " * indent + self.keyword)
        if self.continuation is not None:
            self.continuation.printTree(indent)
        
    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.lvalue.printTree(indent + 1)
        self.operation.printTree(indent + 1)

    @addToClass(AST.Operation)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.left.printTree(indent+1)
        if self.right is not None:
            self.right.printTree(indent+1)

    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.WhileLooping)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.condition.printTree(indent+1)
        self.body.printTree(indent+2)

    @addToClass(AST.ForLooping)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        self.iterator.printTree(indent + 1)
        print("| " * (indent + 1) + "RANGE")
        self.start.printTree(indent + 2)
        self.end.printTree(indent + 2)
        self.body.printTree(indent + 3)

    @addToClass(AST.IfStatement)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.condition.printTree(indent + 1)
        self.body.printTree(indent + 2)
        if self.else_body is not None:
            print("| " * indent + "ELSE")
            self.else_body.printTree(indent + 1)

    @addToClass(AST.Actions)
    def printTree(self, indent=0):
        for action in self.series:
            action.printTree(indent)

    