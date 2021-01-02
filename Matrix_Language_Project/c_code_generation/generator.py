import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from frontend import type_checker
from frontend import symbol_table
from frontend import AST
from c_code_generation import generator_utils as gu
from c_code_generation import matrix_utils as mu

class NodeVisitor(object):
    
    def visit(self, node, indent: int):
        method_name = 'visit' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, indent)

    def generic_visit(self, node, indent: int):
        generated_code = str()
        if isinstance(node, list):
            for child in node:
                generated_code += self.visit(child, indent)
        else:
            for _, attr in node.__dict__.items():
                if isinstance(attr, list):
                    generated_code += self.generic_visit(attr, indent)
                elif issubclass(attr.__class__, AST.Node):
                    generated_code += self.visit(attr, indent)
        return generated_code

class CodeGenerator(NodeVisitor):

    def __init__(self):
        self.symbol_table = symbol_table.SymbolTable()
        self.type_checker = type_checker.TypeChecker(self.symbol_table)

    def visitInteger(self, node: AST.Integer, indent):
        return node.value

    def visitFloat(self, node: AST.Float, indent):
        return node.value

    def visitString(self, node: AST.String, indent):
        return f'{node.value}'

    def visitVariable(self, node: AST.Variable, indent):
        return node.name

    def visitUnaryVariable(self, node: AST.UnaryVariable, indent):
        return node.operator + self.visit(node.value, indent)

    def visitMatrixInitializer(self, node: AST.MatrixInitializer, indent):
        return mu.matrix_initializers_dict[node.keyword](int(self.visit(node.operation, indent)))

    def visitSequence(self, node: AST.Sequence, indent):
        result = str()
        for element in node.elements:
            result += self.visit(element, indent) + ', '
        return result[:-2]

    def visitList(self, node: AST.List, indent):
        return '{' + self.visit(node.sequence, indent) + '}'

    def visitMatrixElement(self, node: AST.MatrixElement, indent):
        dim = '{' + self.visit(node.indexing_sequence, indent) + '}'
        dim_size = str(len([self.visit(element, indent) for element in node.indexing_sequence.elements]))
        return mu.resolve_matrix_element_dereference(', '.join([self.visit(node.identifier, indent), mu.INT_PTR + dim, dim_size]))

    def visitKeyWordInstruction(self, node: AST.KeyWordInstruction, indent):
        continuation = self.visit(node.continuation, indent) if node.continuation is not None else None
        continuation_type = self.type_checker.visit(node.continuation) if node.continuation is not None else None
        return gu.keyword_dict[node.keyword](continuation, continuation_type, indent)
    
    def visitAssignment(self, node: AST.Assignment, indent):
        result = '\t' * indent
        right_type = self.type_checker.visit(node.operation)
        variable_name = node.lvalue.name if isinstance(node.lvalue, AST.Variable) else node.lvalue.identifier.name
        right_side = self.visit(node.operation, indent)
        if isinstance(right_type, list):
            return result + mu.resolve_matrix_assignment(self.symbol_table, variable_name, right_side, node.operator,
            self.type_checker.visit(node.operation))
        if self.symbol_table.get(variable_name) is None:
            result += gu.types_dict[right_type] + ' ' + variable_name
            self.symbol_table.put(variable_name, right_type)
        elif isinstance(node.lvalue, AST.MatrixElement):
            return result + mu.resolve_matrix_element_assignment(self.visit(node.lvalue, indent), right_side, node.operator)
        else:
            result += variable_name
        return result + ' ' + node.operator + ' ' + right_side + ';\n' 

    def visitOperation(self, node: AST.Operation, indent):
        if node is None:
            return

        left_side = self.visit(node.left, indent)
        right_side = self.visit(node.right, indent) if node.right is not None else None

        left_type = self.type_checker.visit(node.left)
        right_type = self.type_checker.visit(node.right) if node.right is not None else None

        if isinstance(node.left, AST.MatrixElement):
            left_side = mu.resolve_matrix_element_dereference(left_side)
        if isinstance(node.right, AST.MatrixElement):
            right_side = mu.resolve_matrix_element_dereference(right_side)

        if isinstance(node.left, AST.Operation):
            left_side = '(' + left_side + ')'
        if isinstance(node.right, AST.Operation):
            right_side = '(' + right_side + ')'
        
        if not isinstance(left_type, list) and not isinstance(right_type, list):
            return ' '.join([left_side, node.operator, right_side])
            
        return mu.resolve_matrix_operation(left_side, left_type, node.operator, right_side, right_type)

    def visitCondition(self, node: AST.Condition, indent):
        return self.visit(node.left, indent) + ' ' + node.operator + ' ' + self.visit(node.right, indent)

    def visitForLooping(self, node: AST.ForLooping, indent):
        self.symbol_table.pushScope('for_looping')
        iterator = self.visit(node.iterator, indent)
        iter_type = self.type_checker.visit(node.start)
        self.symbol_table.put(iterator, iter_type)
        start = self.visit(node.start, indent)
        end = self.visit(node.end, indent)
        body = self.visit(node.body, indent + 1)
        self.symbol_table.popScope()
        return gu.for_loop_to_string(iterator, iter_type, start, end, body, indent)

    def visitWhileLooping(self, node: AST.WhileLooping, indent):
        self.symbol_table.pushScope('while_looping')
        condition = self.visit(node.condition, indent)
        body = self.visit(node.body, indent + 1)
        self.symbol_table.popScope()
        return gu.while_loop_to_string(condition, body, indent)

    def visitIfStatement(self, node: AST.IfStatement, indent):
        self.symbol_table.pushScope('if_statement')
        condition = self.visit(node.condition, indent)
        body = self.visit(node.body, indent + 1)
        result = gu.if_to_string(condition, body, indent)
        self.symbol_table.popScope()
        if node.else_body is not None:
            self.symbol_table.pushScope('else')
            else_body = self.visit(node.else_body, indent + 1)
            result += gu.else_to_string(else_body, indent)
            self.symbol_table.popScope()
        return result

    def visitActions(self, node: AST.Actions, indent):
        return self.visit(node.series, indent)

    def generate(self, ast: AST.Node):
        generated_code = self.visit(ast, 1)
        return gu.decorate(generated_code)
