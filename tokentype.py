from enum import Enum, auto

class TokenTypes(Enum):
	INTEGER = auto()
	FLOAT = auto()

	PLUS = auto()
	MINUS = auto()
	MUL = auto()
	DIV = auto()

	ROOT = auto() # symbol: #
	POW = auto() # symbol: ^
	ROUND = auto() # symbol: ~
	BANG = auto() # symbol: !
	PIPE = auto() # symbol: |

	LPAREN = auto()
	RPAREN = auto()
	
	EOF = -1