from frontend.symbol_table import SymbolTable
from frontend.symbol_table import VariableSymbol

from frontend import AST
from frontend import error_message


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for child in node:
                self.visit(child)
        else:
            for _, attr in node.__dict__.items():
                if isinstance(attr, list):
                    self.generic_visit(attr)
                elif issubclass(attr.__class__, AST.Node):
                    self.visit(attr)

class TypeChecker(NodeVisitor):
    def __init__(self, symbol_table: SymbolTable):
        self.symbol_table = symbol_table

        self.operation_types = {
                ('Integer', 'Integer'): 'Integer', 
                ('Float', 'Float'): 'Float', 
                ('Integer', 'Float'): 'Float', 
                ('Float', 'Integer'): 'Float', 
            }

        self.reserved_matrix_operators = ['.+', '.-', '.*', './', "'"]
        self.allowed_matrix_operators = ['.+', '.-', '.*', './', "'", '*', '*=', '+=', '-=', '/=']

    @staticmethod
    def _unpack_nested_list(nested_list, output):
        for i in nested_list: 
            if type(i) == list: 
                TypeChecker._unpack_nested_list(i, output) 
            else: 
                output.append(i)

    @staticmethod
    def _transpose_matrix(type_size, lineno):
        if not isinstance(type_size[0], list) or isinstance(type_size[0][0], list):
            return error_message.TransposeError(lineno)
        return [[AST.Float.__name__ for _ in type_size] for _ in type_size[0]]

    @staticmethod
    def _matrix_depth(matrix):
        depth = 0
        while isinstance(matrix, list):
            depth +=1
            matrix = matrix[0]

        return depth

    def refactorList(self, list_type):
        if isinstance(list_type, list):
            for inner_list in list_type:
                inner_list = self.refactorList(inner_list)
        return [elem if elem != AST.Integer.__name__ else AST.Float.__name__ for elem in list_type]


    def getVectorVectorOperationType(self, left_side, right_side, operator, lineno):
        if len(left_side) != len(right_side):
                return error_message.TypeMismatch(lineno)
        if operator in ['*', '*=']:
            return [AST.Float.__name__] 
        else:
            return [AST.Float.__name__ for idx in range(len(left_side))]

    def getVectorMatrixOperationType(self, matrix_side, vector_side, operator, lineno):
        if len(matrix_side[0]) != len(vector_side) or operator not in ['*', '*=']:
            return error_message.TypeMismatch(lineno)
        return [AST.Float.__name__ in vector_side for _ in vector_side]

    def getListOperationType(self, left_side, right_side, operator, lineno):
        if TypeChecker._matrix_depth(left_side) > 2 and TypeChecker._matrix_depth(right_side) > 2 and operator == '*':
            return error_message.MatrixMultiplicationError(lineno)
        if operator not in self.allowed_matrix_operators:
            return error_message.ScalarOperatorMisuse(lineno)
        if right_side is None:
            return TypeChecker._transpose_matrix(left_side, lineno)
        if not isinstance(left_side[0], list) and not isinstance(right_side[0], list):
            return self.getVectorVectorOperationType(left_side, right_side, operator, lineno)
        if not isinstance(left_side[0], list):
            return self.getVectorMatrixOperationType(right_side, left_side, operator, lineno)
        if not isinstance(right_side[0], list):
            return self.getVectorMatrixOperationType(left_side, right_side, operator, lineno)
        if operator in ['*']:
            if len(left_side[0]) != len(right_side):
                return error_message.TypeMismatch(lineno)
            return [[AST.Float.__name__ for _ in right_side[0]] for _ in left_side]
        if len(left_side) != len(right_side) or len(left_side[0]) != len(right_side[0]):
            return error_message.TypeMismatch(lineno)
        return [[AST.Float.__name__ for _ in right_side[0]] for _ in right_side]

    def getOperationType(self, left_side, right_side, operator, lineno):
        if isinstance(left_side, list) or isinstance(right_side, list):
            return self.getListOperationType(left_side, right_side, operator, lineno)
        if operator in self.reserved_matrix_operators:
            return error_message.MatrixOperatorMisuse(lineno)
        return self.operation_types.get((left_side, right_side), error_message.TypeMismatch(lineno))

    def visitInteger(self, node: AST.Integer):
        return node.__class__.__name__

    def visitFloat(self, node: AST.Float):
        return node.__class__.__name__

    def visitString(self, node: AST.String):
        return node.__class__.__name__

    def visitVariable(self, node: AST.Variable):
        variable = self.symbol_table.get(node.name)
        if variable is None:
            return error_message.UnitializedAccess(node.lineno)    
        return variable.type_info
    
    def visitUnaryVariable(self, node: AST.UnaryVariable):
        return self.visit(node.value)

    def visitSequence(self, node: AST.Sequence):
        return [self.visit(element) for element in node.elements]

    def visitList(self, node: AST.List):
        visited_sequence = self.visit(node.sequence)
        inner_lists = set([len(element) for element in visited_sequence if isinstance(element, list)])
        if len(inner_lists) not in [0, 1]:
            return error_message.SizeMismatch(node.lineno)
        return self.refactorList(visited_sequence)

    def visitMatrixElement(self, node: AST.MatrixElement):
        if not isinstance(node.identifier, AST.Variable):
            return error_message.InvalidDereferencing(node.lineno)
            
        index_sequence = node.indexing_sequence.elements
        variable = self.symbol_table.get(node.identifier.name)
        if variable is None:
            return error_message.UnitializedAccess(node.lineno)
        variable_type = variable.type_info
        if not isinstance(variable_type, list):
            return error_message.NotIndexable(node.lineno)
        if set([self.visit(elem) for elem in index_sequence]) != set([AST.Integer.__name__]):
            return error_message.InvalidIndexing(node.lineno)
        if set([elem.__class__.__name__ for elem in index_sequence]) != set([AST.Integer.__name__]):
            return AST.Float.__name__
        type_repr = variable_type
        for idx in [int(elem.value) for elem in index_sequence]:
            if len(type_repr) <= idx or not isinstance(type_repr, list):
                return error_message.ListOutOfIndex(node.lineno)
            type_repr = type_repr[idx]
        return type_repr

    def visitMatrixInitializer(self, node: AST.MatrixInitializer):
        if node.operation.__class__ != AST.Integer:
            return error_message.InvalidInitializer(node.lineno)
        return [[AST.Float.__name__ for _ in range(int(node.operation.value))] for _ in range(int(node.operation.value))]

    def visitKeyWordInstruction(self, node: AST.KeyWordInstruction):
        if node.keyword in ['break', 'continue'] and self.symbol_table.searchScopeOfName(['while_looping', 'for_looping']) is None:
            return error_message.KeyWordInstructionOutOfScope(node.lineno)
        if node.keyword == 'print':
            errors = self.visit(node.continuation)
            if len([error for error in errors if isinstance(error, list)]) :
                errors.append(error_message.MatrixInPrint(node.lineno))
            errors = [error for error in errors if error is not None and not isinstance(error, str) and not isinstance(error, list)]
            if errors != []:
                return errors
        if node.keyword == 'return':
            operation_type = self.visit(node.continuation)
            if isinstance(operation_type.__class__, error_message.ErrorMessage):
                return operation_type
        if node.keyword == 'print_matrix':
            operation_type = self.visit(node.continuation)
            if isinstance(operation_type.__class__, error_message.ErrorMessage):
                return operation_type

            if not isinstance(operation_type, list):
                return error_message.InvalidPrintMatrixArgument(node.lineno)

    def visitAssignment(self, node: AST.Assignment):
        operation_type = self.visit(node.operation)
        if issubclass(operation_type.__class__, error_message.ErrorMessage):
            return operation_type
        if isinstance(node.lvalue, AST.MatrixElement):
            matrix_element_type = self.visit(node.lvalue)
            if issubclass(matrix_element_type.__class__, error_message.ErrorMessage):
                return matrix_element_type
            elif (matrix_element_type, operation_type) not in self.operation_types:
                return error_message.TypeMismatch(node.lineno)
        else:
            variable = self.symbol_table.get(node.lvalue.name)
            if variable is None and node.operator != '=':
                return error_message.UnitializedAccess(node.lineno)
            elif node.operator == '=': 
                if variable is not None and variable.type_info != operation_type and not isinstance(operation_type, list) and not isinstance(variable.type_info, list):
                    return error_message.TypeReassignment(node.lineno)
                self.symbol_table.put(node.lvalue.name, operation_type)
            else:
                assignment_type = self.getOperationType(variable.type_info, operation_type, node.operator, node.lineno)
                if issubclass(assignment_type.__class__, error_message.ErrorMessage):
                    return assignment_type
                self.symbol_table.put(variable.name, assignment_type)

    def visitOperation(self, node: AST.Operation):
        left_type = self.visit(node.left)
        if issubclass(left_type.__class__, error_message.ErrorMessage):
            return left_type
        right_type = self.visit(node.right) if node.right is not None else None
        if issubclass(right_type.__class__, error_message.ErrorMessage):
            return right_type
        operator = node.operator
        return self.getOperationType(left_type, right_type, operator, node.lineno)

    def visitCondition(self, node: AST.Condition):
        left_side_type = self.visit(node.left)
        right_side_type = self.visit(node.right)
        if issubclass(left_side_type.__class__, error_message.ErrorMessage):
            return left_side_type
        if issubclass(right_side_type.__class__, error_message.ErrorMessage):
            return right_side_type
        if node.operator not in ['==', '!='] and (isinstance(left_side_type, list) or isinstance(right_side_type, list)):
            return error_message.TypeMismatch(node.lineno)
        
    def visitForLooping(self, node: AST.ForLooping):
        self.symbol_table.pushScope('for_looping')
        start_type = self.visit(node.start)
        errors = [start_type]
        self.symbol_table.put(node.iterator.name, start_type)
        errors.append(self.visit(node.end))
        errors.append(self.visit(node.body) if node.body is not None else None)
        errors = [error for error in errors if error is not None and not isinstance(error, str)]
        self.symbol_table.popScope()
        if errors != []:
            return errors

    def visitWhileLooping(self, node: AST.WhileLooping):
        self.symbol_table.pushScope('while_looping')
        errors = [self.visit(node.condition), self.visit(node.body)]
        errors = [error for error in errors if error is not None]
        self.symbol_table.popScope()
        if errors != []:
            return errors

    def visitIfStatement(self, node: AST.IfStatement):
        self.symbol_table.pushScope('if_statement')
        errors = [self.visit(node.condition), self.visit(node.body)]
        self.symbol_table.popScope()
        if node.else_body is not None:
            if not isinstance(node.else_body, AST.IfStatement):
                self.symbol_table.pushScope('else')
                errors.append(self.visit(node.else_body))
                self.symbol_table.popScope()
            else:
                errors.append(self.visit(node.else_body))
        errors = [error for error in errors if error is not None]
        if errors != []:
            return errors

    def visitActions(self, node: AST.Actions):
        errors = [self.visit(action) for action in node.series]
        result = []
        TypeChecker._unpack_nested_list([error for error in errors if error is not None], result)
        return result
