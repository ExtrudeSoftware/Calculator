class Token:
	def __init__(self, tokentype, value, line, column, index):
		self.tokentype = tokentype
		self.value = value
		self.line = line
		self.column = column
		self.index = index
	
	def __str__(self): return f"Token: tokentype: {self.tokentype}, value: {self.value}, line: {self.line}, column: {self.column}, index: {self.index}"

	def __repr__(self): return str(self)