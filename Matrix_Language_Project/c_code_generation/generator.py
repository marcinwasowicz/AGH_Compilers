import sys
import os

sys.path.insert(0, os.path.abspath('..'))

from frontend import type_checker
from frontend import symbol_table
from frontend import AST
from c_code_generation import generator_utils as gu
from c_code_generation import matrix_utils as mu
from c_code_generation import garbage_collector
from c_code_generation import array_stack

class NodeVisitor(object):
    
    def visit(self, node, indent: int, garbage_collectable=False):
        method_name = 'visit' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, indent, garbage_collectable)

    def generic_visit(self, node, indent: int, garbage_collectable=False):
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
        self.garbage_collector = garbage_collector.GarbageCollector()
        self.array_stack = array_stack.ArrayStack()

    def visitInteger(self, node: AST.Integer, indent, garbage_collectable=False):
        return node.value

    def visitFloat(self, node: AST.Float, indent, garbage_collectable=False):
        return node.value

    def visitString(self, node: AST.String, indent, garbage_collectable=False):
        return f'{node.value}'

    def visitVariable(self, node: AST.Variable, indent, garbage_collectable=False):
        return node.name

    def visitUnaryVariable(self, node: AST.UnaryVariable, indent, garbage_collectable=False):
        return node.operator + self.visit(node.value, indent)

    def visitMatrixInitializer(self, node: AST.MatrixInitializer, indent, garbage_collectable=False):
        return mu.matrix_initializers_dict[node.keyword](int(self.visit(node.operation, indent)), garbage_collectable)

    def visitSequence(self, node: AST.Sequence, indent, garbage_collectable=False):
        result = str()
        for element in node.elements:
            result += self.visit(element, indent) + ', '
        return result[:-2]

    def visitList(self, node: AST.List, indent, garbage_collectable=False):
        return '{' + self.visit(node.sequence, indent) + '}'

    def visitMatrixElement(self, node: AST.MatrixElement, indent, garbage_collectable=False):
        dim = '{' + self.visit(node.indexing_sequence, indent) + '}'
        dim_size = str(len([self.visit(element, indent) for element in node.indexing_sequence.elements]))
        return mu.resolve_matrix_element_dereference(', '.join([self.visit(node.identifier, indent), self.array_stack.handle_request(mu.INT_PTR, dim), dim_size]))

    def visitKeyWordInstruction(self, node: AST.KeyWordInstruction, indent, garbage_collectable=False):
        continuation = self.visit(node.continuation, indent) if node.continuation is not None else None
        continuation_type = self.type_checker.visit(node.continuation) if node.continuation is not None else None
        return gu.keyword_dict[node.keyword](continuation, continuation_type, indent)
    
    def visitAssignment(self, node: AST.Assignment, indent, garbage_collectable=False):
        result = '\t' * indent
        right_type = self.type_checker.visit(node.operation)
        variable_name = node.lvalue.name if isinstance(node.lvalue, AST.Variable) else node.lvalue.identifier.name
        right_side = self.visit(node.operation, indent, garbage_collectable=True)
        if isinstance(right_type, list):
            return result + mu.resolve_matrix_assignment(self.symbol_table, variable_name, right_side, node.operator,
            self.type_checker.visit(node.operation), self.garbage_collector, indent, self.array_stack)
        if self.symbol_table.get(variable_name) is None:
            result += gu.types_dict[right_type] + ' ' + variable_name
            self.symbol_table.put(variable_name, right_type)
        elif isinstance(node.lvalue, AST.MatrixElement):
            return result + mu.resolve_matrix_element_assignment(self.visit(node.lvalue, indent), right_side, node.operator)
        else:
            result += variable_name
        return result + ' ' + node.operator + ' ' + right_side + ';\n' 

    def visitOperation(self, node: AST.Operation, indent, garbage_collectable=False):
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
            
        return mu.resolve_matrix_operation(left_side, left_type, node.operator, right_side, right_type,self.array_stack,garbage_collectable)

    def visitCondition(self, node: AST.Condition, indent, garbage_collectable=False):
        return self.visit(node.left, indent) + ' ' + node.operator + ' ' + self.visit(node.right, indent)

    def visitForLooping(self, node: AST.ForLooping, indent, garbage_collectable=False):
        self.symbol_table.pushScope('for_looping')
        iterator = self.visit(node.iterator, indent)
        iter_type = self.type_checker.visit(node.start)
        self.symbol_table.put(iterator, iter_type)
        start = self.visit(node.start, indent)
        end = self.visit(node.end, indent)
        self.array_stack.init_scope()
        body = self.visit(node.body, indent + 1)
        body += self.garbage_collector.purify_curr_scope(self.symbol_table.getCurrScope(), indent + 1)
        body = self.array_stack.resume_scope(indent + 1) + body
        self.symbol_table.popScope()
        return gu.for_loop_to_string(iterator, iter_type, start, end, body, indent)

    def visitWhileLooping(self, node: AST.WhileLooping, indent, garbage_collectable=False):
        self.symbol_table.pushScope('while_looping')
        condition = self.visit(node.condition, indent)
        self.array_stack.init_scope()
        body = self.visit(node.body, indent + 1)
        body += self.garbage_collector.purify_curr_scope(self.symbol_table.getCurrScope(), indent + 1)
        body = self.array_stack.resume_scope(indent + 1) + body
        self.symbol_table.popScope()
        return gu.while_loop_to_string(condition, body, indent)

    def visitIfStatement(self, node: AST.IfStatement, indent, garbage_collectable=False):
        self.symbol_table.pushScope('if_statement')
        condition = self.visit(node.condition, indent)
        self.array_stack.init_scope()
        body = self.visit(node.body, indent + 1)
        body += self.garbage_collector.purify_curr_scope(self.symbol_table.getCurrScope(), indent + 1)
        body = self.array_stack.resume_scope(indent + 1) + body
        result = gu.if_to_string(condition, body, indent)
        self.symbol_table.popScope()
        if node.else_body is not None:
            self.symbol_table.pushScope('else')
            self.array_stack.init_scope()
            else_body = self.visit(node.else_body, indent + 1)
            else_body += self.garbage_collector.purify_curr_scope(self.symbol_table.getCurrScope(), indent + 1)
            else_body = self.array_stack.resume_scope(indent + 1) + else_body
            result += gu.else_to_string(else_body, indent)
            self.symbol_table.popScope()
        return result

    def visitActions(self, node: AST.Actions, indent, garbage_collectable=False):
        return self.visit(node.series, indent)

    def generate(self, ast: AST.Node):
        generated_code = self.visit(ast, 1)
        generated_code += self.garbage_collector.purify_curr_scope(self.symbol_table.getCurrScope(), 1)
        generated_code = self.array_stack.resume_scope(1) + generated_code
        return gu.decorate(generated_code)
