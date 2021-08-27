"""
Usage

3.14 * 2		= 6.28
2#49			= 7
7^2				= 49

x#y = y ** (1/x)
"""

from tokentype import TokenTypes
from error import Error
from token import Token
from tree import *

class Parser:
	def __init__(self, filename, source, tokens):
		self.hadError = False

		self.filename = filename
		self.source = source
		self.tokens = tokens
		self.index = 0

	def parse(self):
		if not self.isAtEnd():
			return self.expr()

	def expr(self):
		""" expr -> term """

		""" term """
		return self.term()
	
	def term(self):
		""" term -> factor ( ( "+" | "-" ) factor )* """

		""" factor """
		expr =self.factor()

		""" ( ( "+" | "-" ) factor )* """
		while self.match(TokenTypes.PLUS, TokenTypes.MINUS):
			# match method calls advance method
			op = self.peek(-1) # get the previous token
			right = self.factor()
			expr = BinOp(expr, op, right, self.peek().line)

		return expr
	
	def factor(self):
		""" factor -> unary ( ( "/" | "*" | "#" | "^" ) unary )* """
		
		""" unary """
		expr = self.unary()

		""" ( ( "/" | "*" | "#" | "^" ) unary )* """
		while self.match(TokenTypes.DIV, TokenTypes.MUL, TokenTypes.ROOT, TokenTypes.POW):
			op = self.peek(-1)
			right = self.unary()
			expr = BinOp(expr, op, right, self.peek().line)
		
		return expr
	
	def unary(self):
		""" unary -> ( ( "-" | "~" ) unary ) | primary """

		""" ( ( "-" | "~" ) unary ) """
		while self.match(TokenTypes.MINUS, TokenTypes.ROUND):
			op = self.peek(-1)
			right = self.unary()
			return Unary(op, right, self.peek().line)
		
		return self.primary()
	
	def primary(self):
		""" primary -> NUMBER | "(" expr ")" """

		""" NUMBER """
		if self.match(TokenTypes.INTEGER, TokenTypes.FLOAT):
			return Literal(self.peek(-1).value, self.peek().line)
		
		elif self.match(TokenTypes.LPAREN):
			expr = self.expr()
			self.expect(TokenTypes.RPAREN)
			return Grouping(expr, self.peek().line)
		
		# error
		self.error("Syntax Error: Expected expression.")

	### Helper methods

	def match(self, *args):
		for tokentype in args:
			if self.check(tokentype):
				self.advance()
				return True
		
		return False
	
	def expect(self, tokentype):
		if self.check(tokentype):
			return self.advance()

		peek = self.peek()

		# error
		self.error(f"Syntax Error: Expected token type, {tokentype}.")

	def check(self, tokentype):
		if self.isAtEnd(): return False

		return self.peek().tokentype == tokentype
	
	def advance(self):
		if not self.isAtEnd():
			self.index += 1
		
		return self.peek(-1)
	
	def isAtEnd(self):
		return self.peek().tokentype == TokenTypes.EOF
	
	def peek(self, n=0):
		return self.tokens[self.index + n]
	
	def error(self, message):
		peek = self.peek()
	
		Error.pretty_error(self.filename, self.source.split("\n")[peek.line - 1], peek.line, peek.column, message)
		self.hadError = True
