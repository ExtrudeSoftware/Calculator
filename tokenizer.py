from tokentype import TokenTypes
from token import Token
from error import Error

class Tokenizer:
	def __init__(self, filename, source):
		self.hadError = False

		self.filename = filename
		self.source = source

		self.column = 0
		self.start = 0
		self.index = 0
		self.line = 1

		self.tokens = []
	
	def getTokens(self):
		while not self.isAtEnd() and not self.hadError:
			self.start = self.index

			self.getToken()

			self.advance()
		
		self.addToken(TokenTypes.EOF, None)

		return self.tokens

	def getToken(self):
		c = self.peek() # current char

		chars = {
			"+": (lambda: self.addToken(TokenTypes.PLUS, self.source[self.index])),
			"-": (lambda: self.addToken(TokenTypes.MINUS, self.source[self.index])),
			"*": (lambda: self.addToken(TokenTypes.MUL, self.source[self.index])),
			"/": (lambda: self.comment() if self.match("/") else self.addToken(TokenTypes.DIV, self.source[self.index])),

			"(": (lambda: self.addToken(TokenTypes.LPAREN, self.source[self.index])),
			")": (lambda: self.addToken(TokenTypes.RPAREN, self.source[self.index])),

			"#": (lambda: self.addToken(TokenTypes.ROOT, self.source[self.index])),
			"^": (lambda: self.addToken(TokenTypes.POW, self.source[self.index])),
			"~": (lambda: self.addToken(TokenTypes.ROUND, self.source[self.index])),
		}

		if chars.get(c):
			chars[c]()
		
		else:
			if c.isspace():
				if c == "\n":
					self.newline()
				
			elif self.isNumeric(c) or c == ".":
				self.number()
			
			else:
				self.error("Tokenizer Error: Unexpected char.")

	### Helper methods

	def match(self, c):
		if not self.isAtEnd():
			return self.peek(1) == c

	def comment(self):
		while not self.isAtEnd() and self.peek() != "\n":
			self.advance()

	def newline(self):
		self.column = 0
		self.line += 1

	def number(self):
		dot = False

		while not self.isAtEnd() and (self.isNumeric(self.peek()) or self.peek() == "."):
			if self.peek() == ".":
				dot = True if not dot else self.error("Tokenizer Error: Unexpected dot.")
			
			self.advance()
		
		if dot:
			# float
			self.addToken(TokenTypes.FLOAT, float(self.source[self.start: self.index]))
		
		else:
			# integer
			self.addToken(TokenTypes.INTEGER, int(self.source[self.start: self.index]))
		
		self.index -= 1

	def isNumeric(self, c):
		return c >= "0" and c <= "9"

	def error(self, message):
		Error.pretty_error(self.filename, self.source.split("\n")[self.line - 1], self.line, self.column, message)
		self.hadError = True 

	def isAtEnd(self):
		return self.index >= len(self.source)
	
	def peek(self, i=0):
		return self.source[self.index + i]
	
	def advance(self):
		if not self.isAtEnd():
			self.index += 1
			self.column += 1

	def addToken(self, tokentype, value):
		self.tokens.append(Token(tokentype, value, self.line, self.column, self.index))