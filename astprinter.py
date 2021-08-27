from tree import *

class AstPrinter:
	def pretty_print(self, expr):
		print(expr.accept(self))

	def visit(self, expr):
		if isinstance(expr, BinOp):
			return self.visit_binop(expr)
		
		elif isinstance(expr, Literal):
			return self.visit_literal(expr)
		
		elif isinstance(expr, Unary):
			return self.visit_unary(expr)
		
		elif isinstance(expr, Grouping):
			return self.visit_grouping(expr)
	
	def visit_binop(self, expr):
		left = expr.left.accept(self)
		op = expr.op
		right = expr.right.accept(self)

		return f"(BinOp: left: {left}, op: {op}, right: {right}, line: {expr.line})"

	def visit_literal(self, expr):
		return f"(Literal: value: {expr.value}, line: {expr.line})"
	
	def visit_unary(self, expr):
		right = expr.right.accept(self)
		return f"(Unary: op: {expr.op}, right: {right}, line: {expr.line})"
	
	def visit_grouping(self, expr):
		e = expr.expr.accept(self)
		return f"(Grouping: expr: {e}, line: {expr.line})"