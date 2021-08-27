from tokentype import TokenTypes
from tree import *
from error import Error

import math

class Interpreter:
	def __init__(self, filename, source, ast):
		self.hadError = False

		self.filename = filename
		self.source = source
		self.ast = ast
	
	def interpret(self):
		if self.ast:
			return self.ast.accept(self)

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
		op = expr.op.tokentype
		right = expr.right.accept(self)

		if self.match(op, TokenTypes.PLUS):
			return left + right
		
		elif self.match(op, TokenTypes.MINUS):
			return left - right
		
		elif self.match(op, TokenTypes.MUL):
			return left * right
		
		elif self.match(op, TokenTypes.DIV):
			# check if right is 0
			
			if right == 0:
				return self.error(expr.line, "Runtime Error: Cannot divide by zero.")
			
			else:
				return left / right
		
		elif self.match(op, TokenTypes.POW):
			return left ** right
		
		elif self.match(op, TokenTypes.ROOT):
			# x#y = y ** (1/x)
			return right ** (1 / left)
		
		elif self.match(op, TokenTypes.ROUND):
			print(left, op, right)

	def visit_literal(self, expr):
		return expr.value
	
	def visit_unary(self, expr):
		op = expr.op.tokentype
		right = expr.right.accept(self)

		if op == TokenTypes.MINUS:
			return right * -1
		
		elif op == TokenTypes.ROUND:
			return round(right)
		
		elif op == TokenTypes.BANG:
			return math.factorial(right)
	
	def visit_grouping(self, expr):
		return expr.expr.accept(self)
	
	### Helper methods

	def match(self, token, *tokentypes):
		for tokentype in tokentypes:
			if token == tokentype:
				return True
		
		return False
	
	def error(self, line, message):
		# throw a runtime error
		Error.error(self.filename, self.source.split("\n")[line - 1], line, message)
		self.hadError = True