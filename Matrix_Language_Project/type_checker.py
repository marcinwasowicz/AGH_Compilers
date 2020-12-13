from symbol_table import SymbolTable
from symbol_table import VariableSymbol

import AST
import error_message


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

    @staticmethod
    def _unpack_nested_list(nested_list, output):
        for i in nested_list: 
            if type(i) == list: 
                TypeChecker._unpack_nested_list(i, output) 
            else: 
                output.append(i)

    def getVectorVectorOperationType(self, left_side, right_side, operator):
        if len(left_side) != len(right_side):
                return error_message.TypeMismatch(self.symbol_table.getParentScope())
        if operator in ['*', '*=']:
            return [AST.Float.__name__] if AST.Float.__name__ in left_side or AST.Float.__name__ in left_side else [AST.Integer.__name__]
        else:
            return [self.operation_types[(left_side[idx], right_side[idx])] for idx in range(len(left_side))]

    def getVectorMatrixOperationType(self, matrix_side, vector_side, operator):
        if len(matrix_side[0]) != len(vector_side) or operator not in ['*', '*=']:
            return error_message.TypeMismatch(self.symbol_table.getParentScope())
        return [AST.Float.__name__ in vector_side for _ in vector_side]

    def getListOperationType(self, left_side, right_side, operator):
        if not isinstance(left_side[0], list) and not isinstance(right_side[0], list):
            return self.getVectorVectorOperationType(left_side, right_side, operator)
        if not isinstance(left_side[0], list):
            return self.getVectorMatrixOperationType(right_side, left_side, operator)
        if not isinstance(right_side[0], list):
            return self.getVectorMatrixOperationType(left_side, right_side, operator)
        if operator in ['*', '*=']:
            if len(left_side[0]) != len(right_side):
                return error_message.TypeMismatch(self.symbol_table.getParentScope())
            return [[AST.Float.__name__ for _ in right_side[0]] for _ in left_side[0]]
        if len(left_side) != len(right_side) or len(left_side[0]) != len(right_side[0]):
            return error_message.TypeMismatch(self.symbol_table.getParentScope())
        return [[AST.Float.__name__ for _ in right_side[0]] for _ in right_side]

    def getOperationType(self, left_side, right_side, operator):
        if isinstance(left_side, list) or isinstance(right_side, list):
            return self.getListOperationType(left_side, right_side, operator)
        return self.operation_types.get((left_side, right_side), error_message.TypeMismatch(self.symbol_table.getParentScope()))

    def visitInteger(self, node: AST.Integer):
        return node.__class__.__name__

    def visitFloat(self, node: AST.Float):
        return node.__class__.__name__

    def visitString(self, node: AST.String):
        return node.__class__.__name__

    def visitVariable(self, node: AST.Variable):
        variable = self.symbol_table.get(node.name)
        if variable is None:
            return error_message.UnitializedAccess(node.name, self.symbol_table.getParentScope())    
        return variable.type_info
    
    def visitUnaryVariable(self, node: AST.UnaryVariable):
        return self.visit(node.value)

    def visitSequence(self, node: AST.Sequence):
        return [self.visit(element) for element in node.elements]

    def visitList(self, node: AST.List):
        visited_sequence = self.visit(node.sequence)
        inner_lists = set([len(element) for element in visited_sequence if isinstance(element, list)])
        if len(inner_lists) not in [0, 1]:
            return error_message.SizeMismatch(self.symbol_table.getParentScope())
        return visited_sequence

    def visitMatrixElement(self, node: AST.MatrixElement):
        variable = self.symbol_table.get(node.identifier.name)
        index_sequence = node.indexing_sequence.elements

        if variable is None:
            return error_message.UnitializedAccess(self.symbol_table.getParentScope())
        if not isinstance(variable.type_info, list):
            return error_message.NotIndexable(self.symbol_table.getParentScope())
        if set([elem.__class__.__name__ for elem in index_sequence]) != set([AST.Integer.__name__]):
            return error_message.InvalidIndexing(self.symbol_table.getParentScope())

        type_repr = variable.type_info
        for idx in [int(elem.value) for elem in index_sequence]:
            if len(type_repr) <= idx or not isinstance(type_repr, list):
                return error_message.ListOutOfIndex(self.symbol_table.getParentScope())
            type_repr = type_repr[idx]
        return type_repr

    def visitMatrixInitializer(self, node: AST.MatrixInitializer):
        if node.operation.__class__ != AST.Integer:
            return error_message.InvalidInitializer(self.symbol_table.getParentScope())
        return [[AST.Integer.__name__ for _ in range(int(node.operation.value))] for _ in range(int(node.operation.value))]

    def visitKeyWordInstruction(self, node: AST.KeyWordInstruction):
        if node.keyword in ['break', 'continue'] and self.symbol_table.searchScopeOfName(['while_looping', 'for_looping']) is None:
            return error_message.KeyWordInstructionOutOfScope(self.symbol_table.getParentScope())
        if node.keyword == 'print':
            errors = self.visit(node.continuation)
            errors = [error for error in errors if error is not None and not isinstance(error, str)]
            if errors != []:
                return errors
        if node.keyword == 'return':
            operation_type = self.visit(node.continuation)
            if isinstance(operation_type.__class__, error_message.ErrorMessage):
                return operation_type

    def visitAssignment(self, node: AST.Assignment):
        operation_type = self.visit(node.operation)
        if issubclass(operation_type.__class__, error_message.ErrorMessage):
            return operation_type
        if isinstance(node.lvalue, AST.MatrixElement):
            matrix_element_type = self.visit(node.lvalue)
            if issubclass(matrix_element_type.__class__, error_message.ErrorMessage):
                return matrix_element_type
            elif matrix_element_type != operation_type:
                return error_message.TypeMismatch(self.symbol_table.getParentScope())
        else:
            variable = self.symbol_table.get(node.lvalue.name)
            if variable is None and node.operator != '=':
                return error_message.UnitializedAccess(self.symbol_table.getParentScope())
            elif node.operator == '=':
                self.symbol_table.put(node.lvalue.name, operation_type)
            else:
                assignment_type = self.getOperationType(variable.type_info, operation_type, node.operator)
                if issubclass(assignment_type.__class__, error_message.ErrorMessage):
                    return assignment_type
                self.symbol_table.put(variable.name, assignment_type)

    def visitOperation(self, node: AST.Operation):
        left_type = self.visit(node.left)
        if issubclass(left_type.__class__, error_message.ErrorMessage):
            return left_type
        right_type = self.visit(node.right)
        if issubclass(right_type.__class__, error_message.ErrorMessage):
            return right_type
        operator = node.operator
        return self.getOperationType(left_type, right_type, operator)

    def visitCondition(self, node: AST.Condition):
        left_side_type = self.visit(node.left)
        right_side_type = self.visit(node.right)
        if issubclass(left_side_type.__class__, error_message.ErrorMessage):
            return left_side_type
        if issubclass(right_side_type.__class__, error_message.ErrorMessage):
            return right_side_type
        if node.operator not in ['==', '!='] and (isinstance(left_side_type, list) or isinstance(right_side_type, list)):
            return error_message.TypeMismatch()
        
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
