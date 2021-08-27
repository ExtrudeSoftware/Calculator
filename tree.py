class Ast:
	def accept(self, visitor):
		return visitor.visit(self)

class BinOp(Ast):
	def __init__(self, left, op, right, line):
		self.left = left
		self.op = op
		self.right = right
		self.line = line

class Literal(Ast):
	def __init__(self, value, line):
		self.value = value
		self.line = line

class Unary(Ast):
	def __init__(self, op, right, line):
		self.op = op
		self.right = right
		self.line = line

class Grouping(Ast):
	def __init__(self, expr, line):
		self.expr = expr
		self.line = line